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

# Get all documents from the 'questions' collection
questions_ref = db.collection('questions')
questions = questions_ref.stream()

# Loop through each document and update the 'option' key to 'options'
for doc in questions:
    doc_dict = doc.to_dict()
    for lang in doc_dict:
        if 'option' in doc_dict[lang]:
            doc_dict[lang]['options'] = doc_dict[lang].pop('option')
            doc_ref = questions_ref.document(doc.id)
            doc_ref.set(doc_dict)
            print('updated document', doc.id)

print('Done updating documents')
