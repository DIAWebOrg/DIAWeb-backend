from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .utils.redis_connection import redis_client

class DiabetesPredictionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_data_json['channel_name'] = self.channel_name
        redis_client.xadd('diabetes_predictions', text_data_json)

    async def websocket_send(self, event):
        await self.send(text_data=event['text'])