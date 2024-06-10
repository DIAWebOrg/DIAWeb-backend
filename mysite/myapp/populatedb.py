import os
import sys
import django
from firebase_admin import firestore

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) # add root path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add /mysite path
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

django.setup()

from firebase import db

# Firestore data insertion
def populate_firestore():
    # Create and save instances of Dummy data in Firestore
    dummy_data = [
        {'attributeA': 'Value 1A', 'attributeB': 10, 'attributeC': 'Lorem ipsum'},
        {'attributeA': 'Value 2A', 'attributeB': 20, 'attributeC': 'Dolor sit amet'},
        {'attributeA': 'Value 3A', 'attributeB': 30, 'attributeC': 'Consectetur adipiscing elit'},
        {'attributeA': 'Value 4A', 'attributeB': 40, 'attributeC': 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'}
    ]

    for i, data in enumerate(dummy_data):
        doc_ref = db.collection('dummies').document(f'dummy{i+1}')
        doc_ref.set(data)

if __name__ == '__main__':
    populate_firestore()
