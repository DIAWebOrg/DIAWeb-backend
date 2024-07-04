from channels.generic.websocket import AsyncWebsocketConsumer
import json
import numpy as np
import re
from .utils.Serializer import Serializer
from django.db import transaction
from channels.db import database_sync_to_async
from django.conf import settings
import asyncio

class DiabetesPredictionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # headers is a list of tuples, where each tuple contains the header name and value,
        # so we need to iterate over the list to find the value of the tuple where the header name is 'x-api-key'
        api_key = next((header[1].decode('utf-8') for header in self.scope['headers'] if header[0] == b'x-api-key'), None)
        print('api_key:', api_key)
        evaluation_result = await evaluate_api_key(api_key)

        if evaluation_result['status'] == 200:
            await self.accept()
            # Send the number of remaining requests back to the client
            await self.send(text_data=json.dumps({
                'message': 'Connection accepted',
                'remaining_requests': evaluation_result['remaining_requests']
            }))
        else:
            await self.close(code=evaluation_result['status'])

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json.get('data')
        serializer = Serializer(data=text_data_json)

        if data and serializer.is_valid():
            data = serializer.validated_data['data']
            data = np.array(data).astype('float32').reshape(1, -1)
            # tensorflow keras does not natively support asyncronous operations, so
            # we use asyncio.to_thread to run the predict method in a separate thread asynchronously
            # so it doesnt block the main thread
            prediction = await asyncio.to_thread(settings.MODEL.predict, data)

            await self.send(text_data=json.dumps({
                # Convert numpy array to list for JSON serialization
                'prediction': prediction.tolist()
            }))
        else:
            
            await self.send(text_data=json.dumps({
                'error': 'Invalid data'
            }))

@database_sync_to_async
def evaluate_api_key(api_key):
    # Regex pattern for UUID
    uuid_regex = re.compile(
        r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ABab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$')

    if not api_key:
        print('A')
        return {'error': 'API key required', 'status': 401}
    
    elif not uuid_regex.match(api_key):
        return {'error': 'Invalid API key format', 'status': 400}

    try:
        with transaction.atomic():
            from .models import APIKey # import the model here to avoid "apps aren loaded yet" error
            api_key = APIKey.objects.select_for_update().get(api_key=api_key)

            if api_key.remaining_requests <= 0:
                return {'error': 'Rate limit exceeded', 'status': 429}
            
            else:
                api_key.remaining_requests -= 1
                api_key.save()
                return {'remaining_requests': api_key.remaining_requests, 'status': 200}
        
    except APIKey.DoesNotExist:
        return {'error': 'API key not found', 'status': 404}
