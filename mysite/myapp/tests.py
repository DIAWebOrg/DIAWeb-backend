from django.test import TransactionTestCase, Client
from rest_framework import status
from django.conf import settings
import json
import numpy as np
from .models import APIKey
from channels.testing import WebsocketCommunicator
from django.conf import settings
from .consumers import DiabetesPredictionConsumer


class PredictDiabetesTest(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        # this doesnt have an impact on the real database
        APIKey.objects.create(api_key=settings.API_KEY_TEST)

    async def test_predict_diabetes_websocket(self):

        communicator = WebsocketCommunicator(
            DiabetesPredictionConsumer.as_asgi(), "/ws/predict_diabetes/")
        # connect returns a tuple with a boolean and a response which indicates the status code of the response
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Prepare and send the data through WebSocket
        data = settings.DATAFRAME
        data = data.drop(columns=['CP', 'CP_numero',
                         'CP_codigo', 'meses', 'incidencia'])
        second_row = data.iloc[1]
        features = [int(value) if isinstance(value, np.int64) # type: ignore
                    else value for value in second_row.tolist()]

        # After establishing the connection and sending the data
        await communicator.send_json_to({'data': features, 'action': 'predict_diabetes', 'api_key': settings.API_KEY_TEST})

        # wait for the prediction response
        prediction_response = await communicator.receive_json_from()
        self.assertIn('prediction', prediction_response)

        # Close the connection
        await communicator.disconnect()
