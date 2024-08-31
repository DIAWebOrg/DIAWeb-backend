from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .utils.Serializer import Serializer
import numpy as np
from .models import APIKey
import re

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
    
# i need a method to get the remaining requests of an api key:
class RemainingRequests(APIView):
    def post(self, request):
        api_key = request.data.get('api_key')
        uuid_regex = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ABab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$')

        if not uuid_regex.match(api_key):
            return JsonResponse({'error': 'Invalid license'}, status=400)
    
        try:
            # Query the database to get the API key object
            print("ahquí")
            api_key_obj = APIKey.objects.get(api_key=api_key)
            remaining_requests = api_key_obj.remaining_requests
            return JsonResponse({'remaining_requests': remaining_requests})
        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'license not found'}, status=404)

class IndexView(APIView):

    def get(self, request):
        return HttpResponse("Welcome to my Django project!")


class HelloWorldView(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Hello World'})
