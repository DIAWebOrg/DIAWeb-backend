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
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)

        action = text_data_json.get('action')
        api_key = text_data_json.get('api_key')

        evaluation_result = await evaluate_api_key(api_key, decrement=True)
        remaining_requests = evaluation_result['remaining_requests']

        if action == 'check_remaining_requests':
            await self.send(text_data=json.dumps({
                'remaining_requests': remaining_requests
            }))

        elif action == 'predict_diabetes':
            await self.predict_diabetes(text_data_json, remaining_requests)

    async def predict_diabetes(self, text_data_json, remaining_requests):
        data = text_data_json.get('data')
        serializer = Serializer(data=text_data_json)

        if data and serializer.is_valid() and remaining_requests > 0:
            data = serializer.validated_data['data']  # type: ignore
            data = np.array(data).astype('float32').reshape(1, -1)
            # tensorflow keras does not natively support asyncronous operations, so
            # we use asyncio.to_thread to run the predict method in a separate thread asynchronously
            # so it doesnt block the main thread
            prediction = await asyncio.to_thread(settings.MODEL.predict, data)

            await self.send(text_data=json.dumps({
                # Convert numpy array to list for JSON serialization
                'prediction': prediction.tolist(),
                'remaining_requests': remaining_requests
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
            # import the model here to avoid "apps aren loaded yet" error
            from .models import APIKey
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
