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
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
