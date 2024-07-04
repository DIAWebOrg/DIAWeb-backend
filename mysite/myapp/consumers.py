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
        evaluation_result = await evaluate_api_key(api_key, decrement=True)

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
        action = text_data_json.get('action')

        if action == 'check_remaining_requests':
            await self.check_remaining_requests(text_data_json)
        elif action == 'predict_diabetes':  
            await self.predict_diabetes(text_data_json)

        

    # method to be called in the frontend on initial connection to check the remaining requests
    async def check_remaining_requests(self, text_data_json):
        api_key = text_data_json.get('api_key')
        evaluation_result = await evaluate_api_key(api_key, decrement=False)

        if evaluation_result['status'] == 200:
            await self.send(text_data=json.dumps({
                'message': 'API key is valid',
                'remaining_requests': evaluation_result['remaining_requests']
            }))
        else:
            await self.send(text_data=json.dumps({
                'error': evaluation_result.get('error', 'An error occurred'),
                'status': evaluation_result['status']
            }))

    async def predict_diabetes(self, text_data_json):
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
def evaluate_api_key(api_key, decrement):
    # Regex pattern for UUID
    uuid_regex = re.compile(
        r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ABab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$')

    if not api_key:
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
                if decrement:
                    api_key.remaining_requests -= 1
                    api_key.save()
                return {'remaining_requests': api_key.remaining_requests, 'status': 200}
        
    except APIKey.DoesNotExist:
        return {'error': 'API key not found', 'status': 404}
