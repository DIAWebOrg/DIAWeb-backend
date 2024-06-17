from django.core.management.base import BaseCommand
from myapp.models import APIKey
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Creates a new API key'

    def handle(self, *args, **kwargs):
        new_key = APIKey.objects.create()
        # Construct cache key
        api_key = f"cache_key:{new_key.api_key}"

        remaining_requests = 2
        # insert the data into the cache database as a dictionary entry where the key is the cache_key
        cache.set(api_key, remaining_requests)

        self.stdout.write(self.style.SUCCESS(f'New API key created: {new_key.api_key}'))