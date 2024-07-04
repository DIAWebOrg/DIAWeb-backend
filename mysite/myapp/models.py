from django.db import models
import uuid

class Dummy(models.Model):
    attributeA = models.CharField(max_length=99)
    attributeB = models.IntegerField()
    attributeC = models.TextField()

    def __str__(self):
        return f'{self.attributeA} - {self.attributeB} - {self.attributeC}'


class APIKey(models.Model):
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    remaining_requests = models.IntegerField(default=5)

    def __str__(self):
        return f'{self.api_key} - {self.remaining_requests}'