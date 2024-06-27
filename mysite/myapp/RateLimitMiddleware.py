from django.http import JsonResponse
from .models import APIKey
import os
import re

# this middleware executes before the view.
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key == os.getenv('API_KEY_TEST'):
            return None
        else:
            return evaluate_api_key(api_key)

def evaluate_api_key(api_key):
    # Regex pattern for UUID
    uuid_regex = re.compile(
        r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ABab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$')

    if not api_key:
        return JsonResponse({'error': 'API key required'}, status=401)
    elif not uuid_regex.match(api_key):
        return JsonResponse({'error': 'Invalid API key format'}, status=400)

    try:
        api_key = APIKey.objects.get(api_key=api_key)
        if api_key.remaining_requests <= 0:
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
        else:
            api_key.remaining_requests -= 1
            api_key.save()
    except APIKey.DoesNotExist:
        return JsonResponse({'error': 'API key not found'}, status=404)
