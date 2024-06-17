from django.core.cache import cache
from django.http import JsonResponse
from .models import APIKey
import uuid
import os

# this middleware executes before the view


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        api_key = request.META.get('HTTP_X_API_KEY')  # normal (no prefix)

        if not api_key:
            return JsonResponse({'error': 'API key required'}, status=401)
        # check valid format, existence and rate limit
        try:
            uuid.UUID(api_key)
        except ValueError:
            return JsonResponse({'error': 'Invalid API key format'}, status=400)

        try:
            # present in headers but not in the database
            _ = APIKey.objects.get(api_key=api_key)
        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'Invalid API key'}, status=401)

         # Bypass rate limiting for the test api key
        if api_key == os.getenv('API_KEY_TEST'):
            return None

        # Implement rate limiting
        rate_limit_key = f"api_key_info:{api_key}"
        # 0 is the default value if the key is not found
        remaining_requests = cache.get(rate_limit_key, 0)

        # Allow up to 2 requests
        if remaining_requests <= 0:
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)

        # Update the request count
        cache.decr(rate_limit_key)

        return None
