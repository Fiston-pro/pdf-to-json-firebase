import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from datetime import datetime

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('./firebaseSecret.json')
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()

with open('data.json', 'r', encoding='utf-8') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)

# Upload the questions to Firestore
for key, value in data.items():
    # Create a document reference with the question number as the document ID
    doc_ref = db.collection('questions').document(key)

    # Upload the question data to Firestore
    doc_ref.set({
        'id': key,
        'image':value['image'],
        "kinyarwanda":value['kinyarwanda'],
        "english":value['english'],
        "french":value['french'],
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    print(f'Uploaded question {key} to Firestore')
