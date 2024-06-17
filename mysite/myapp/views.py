from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .utils.Serializer import Serializer
import numpy as np

class PredictDiabetesAPIView(APIView):

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
            data = np.array(data).astype('float32').reshape(1, -1)

            # Make predictions using the loaded model
            prediction = settings.MODEL.predict(data)

            return Response({'prediction': prediction})
        return Response({'errors': serializer.errors}, status=400)


class IndexView(APIView):

    def get(self, request):
        return HttpResponse("Welcome to my Django project!")


class HelloWorldView(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Hello World'})
