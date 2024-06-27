from django.core.management.base import BaseCommand
from myapp.models import APIKey

class Command(BaseCommand):
    help = 'Creates a new API key'

    def handle(self, *args, **kwargs):
        new_key = APIKey.objects.create()
        self.stdout.write(self.style.SUCCESS(f'New API key created: {new_key.api_key}'))