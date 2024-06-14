from django.test import TransactionTestCase, Client
from rest_framework import status
from django.conf import settings
import json
import numpy as np
import pandas as pd


class PredictDigitsTest(TransactionTestCase):
    def setUp(self):
        self.client = Client()

    def test_predict_digits_post(self):
        data = settings.DATAFRAME
        data = data.drop(columns=['CP', 'CP_numero',
                                  'CP_codigo', 'meses', 'incidencia'])
        second_row = data.iloc[1]
        features = [int(value) if isinstance(value, np.int64)
                    else value for value in second_row.tolist()]
        data = {'data': features}
        # Make POST request to the API endpoint
        response = self.client.post(
            '/predict_diabetes', data=json.dumps(data), content_type='application/json')

        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains the 'prediction' key
        self.assertIn('prediction', response.data)
