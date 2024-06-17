from django.core.management.base import BaseCommand
from myapp.models import APIKey
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Creates a new API key'

    def handle(self, *args, **kwargs):
        new_key = APIKey.objects.create()
        # Construct cache key
        cache_key = f"api_key_info:{new_key.key}"

        remaining_requests = 10
        # insert the data into the cache database as a dictionary entry where the key is the cache_key
        cache.set(cache_key, remaining_requests)

        self.stdout.write(self.style.SUCCESS(f'New API key created: {new_key.key}'))