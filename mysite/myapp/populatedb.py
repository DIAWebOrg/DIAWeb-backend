import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

from myapp.models import Dummy

# Create and save instances of the Dummy model
dummy1 = Dummy.objects.create(attributeA='Value 1A', attributeB=10, attributeC='Lorem ipsum')
dummy2 = Dummy.objects.create(attributeA='Value 2A', attributeB=20, attributeC='Dolor sit amet')
dummy3 = Dummy.objects.create(attributeA='Value 3A', attributeB=30, attributeC='Consectetur adipiscing elit')

# You can also save an instance by first creating it and then calling .save()
dummy4 = Dummy(attributeA='Value 4A', attributeB=40, attributeC='Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua')
dummy4.save()