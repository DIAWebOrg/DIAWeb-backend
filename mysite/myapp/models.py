from django.db import models
import uuid

class APIKey(models.Model):
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    remaining_requests = models.IntegerField(default=5)

    def __str__(self):
        return f'{self.api_key} - {self.remaining_requests}'