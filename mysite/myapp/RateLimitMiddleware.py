from django.core.cache import cache
from django.http import JsonResponse
from .models import APIKey
import uuid

# this middleware executes before the view
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return JsonResponse({'error': 'API key required'}, status=401)
        # check valid format, existence and rate limit
        try:
            uuid.UUID(api_key)
        except ValueError:
            return JsonResponse({'error': 'Invalid API key format'}, status=400)

        try:
            api_key_obj = APIKey.objects.get(key=api_key)
        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'Invalid API key'}, status=401)

        # Implement rate limiting
        rate_limit_key = f"rate_limit_{api_key}"
        request_count = cache.get(rate_limit_key, 0)

        # Allow up to 2 requests
        if request_count >= 2:
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)

        # Increment the request count
        cache.set(rate_limit_key, request_count + 1)  # Update the request count (in supabase its transformed to string)

        return None