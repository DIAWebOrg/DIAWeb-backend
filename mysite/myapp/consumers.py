from cgitb import text
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .utils.redis_connection import redis_client

class DiabetesPredictionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # loads converts from string, while dumps converts to string
        text_data_json = json.loads(text_data)
        text_data_json['channel_name'] = self.channel_name
        # redis stream wont accept fields that arent bytes/strings so we transfrom "data" (list of numbers) to string
        # (then in tasks.predict_diabetes we convert it back to a list of numbers with json.loads)
        if 'data' in text_data_json:
            text_data_json['data'] = json.dumps(text_data_json['data'])
        redis_client.xadd('diabetes_predictions', text_data_json)

    async def websocket_send(self, event):
        await self.send(text_data=event['text'])