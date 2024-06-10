# Initialize Firebase to use Firestore
import firebase_admin
from firebase_admin import credentials, firestore

# Path to the downloaded service account key
cred = credentials.Certificate('firebase_config.json')
firebase_admin.initialize_app(cred)

db = firestore.client()