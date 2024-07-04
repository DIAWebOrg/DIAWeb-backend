from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/predict_diabetes/', consumers.DiabetesPredictionConsumer.as_asgi()),
]