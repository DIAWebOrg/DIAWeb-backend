from django.core.cache import cache
from django.http import JsonResponse
import uuid
import os
import re

# this middleware executes before the view. it doesnt acces the normal database (slow) but the cache (faster)
# if the server restarts, the cache is cleared so in production that should not happen
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        api_key = request.META.get('HTTP_X_API_KEY')  # normal (no prefix)

        if api_key == os.getenv('API_KEY_TEST'):
            return None     
        else:
            response, cache_key = is_valid_api_key(api_key)
            if response != True:
                return response
            else:
                cache.decr(cache_key)
                return None

def is_valid_api_key(api_key):
    response = True
    cache_key = None
    # Regex pattern for UUID version 4
    uuid_regex = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ABab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$')
    
    if not api_key:
        response = JsonResponse({'error': 'API key required'}, status=401)
    elif not uuid_regex.match(api_key):
        response = JsonResponse({'error': 'Invalid API key format'}, status=400)
    else:
        cache_key = f"cache_key:{api_key}"
        remaining_requests = cache.get(cache_key)

        if remaining_requests is None:
            response = JsonResponse({'error': 'API key not found'}, status=404)
        elif remaining_requests <= 0:
            response = JsonResponse({'error': 'Rate limit exceeded'}, status=429)
    
    return response, cache_key