from celery import shared_task
from django.conf import settings
import numpy as np
import re
from django.db import transaction
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# TODO: explain this
try:
    from utils.Serializer import Serializer
except ImportError:
    from myapp.utils.Serializer import Serializer

@shared_task
def predict_diabetes(data, remaining_requests):
    serializer = Serializer(data=data)
    if data and serializer.is_valid():
        data = serializer.validated_data['data']  # type: ignore
        data = np.array(data).astype('float32').reshape(1, -1)
        prediction = settings.MODEL.predict(data)
        # return the prediction alongside the remaining requests a a json
        return json.dumps({'prediction': prediction.tolist(), 'remaining_requests': remaining_requests})
    
    else:
        return {'error': 'Invalid data'}
    
@shared_task
def evaluate_api_key(api_key, isPrediction):

    uuid_regex = re.compile(
        r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ABab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$')

    if not api_key:
        return {'error': 'API key required', 'status': 401}

    elif not uuid_regex.match(api_key):
        return {'error': 'Invalid API key format', 'status': 400}

    try:
        with transaction.atomic():
            try:
                from models import APIKey
            except ImportError:
                from myapp.models import APIKey
            api_key_obj = APIKey.objects.select_for_update().get(api_key=api_key)

            if api_key_obj.remaining_requests <= 0:
                return {'error': 'Rate limit exceeded', 'status': 429}

            else:
                if isPrediction:
                    # TODO: migrate to postgre
                    api_key_obj.remaining_requests -= 1
                    api_key_obj.save()

                return {'remaining_requests': api_key_obj.remaining_requests, 'status': 200}

    except APIKey.DoesNotExist:
        return {'error': 'API key not found', 'status': 404}
    
@shared_task
def process_task_result(result, channel_name):
    # send the task result asynchronously back to the WebSocket client
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.send)(channel_name, { # type: ignore
        'type': 'websocket.send',
        'text': json.dumps(result)
    })