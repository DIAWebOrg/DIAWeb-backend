from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .utils.Serializer import Serializer
import numpy as np
import json

class PredictDigitsAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Predict using the NN model",
        operation_description="Post an array of bits named \"data\"",
        request_body=Serializer,
        responses={200: "Success"},
        tags=["Predict"],
    )
    def post(self, request):
        serializer = Serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data['data']
            data = np.array(data).astype('float32')
            data = data.reshape(-1, 28, 28, 1)

            # Make predictions using the loaded model
            predictions = settings.MODEL.predict(data)

            return Response({'predictions': predictions.tolist()})
        return Response(serializer.errors, status=400)

class IndexView(APIView):

    def get(self, request):
        return HttpResponse("Welcome to my Django project!")

class HelloWorldView(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Hello World'})
