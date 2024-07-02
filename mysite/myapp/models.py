from django.db import models
import uuid

# Not using Django's ORM for now since we're using supabase
class Dummy(models.Model):
    attributeA = models.CharField(max_length=99)
    attributeB = models.IntegerField()
    attributeC = models.TextField()

    def __str__(self):
        return f'{self.attributeA} - {self.attributeB} - {self.attributeC}'

    class Meta:
        app_label = 'myapp'

class APIKey(models.Model):
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    remaining_requests = models.IntegerField(default=5)

    def __str__(self):
        return f'{self.api_key} - {self.remaining_requests}'