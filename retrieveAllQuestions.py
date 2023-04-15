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

# Get all the documents in the 'questions' collection
questions_ref = db.collection('questions')
docs = questions_ref.get()

# Convert the Firestore documents to Python dictionaries
data = []
for doc in docs:
    doc_dict = doc.to_dict()
    # Convert Firestore timestamps to datetime objects
    if 'timestamp' in doc_dict:
        timestamp_string = doc_dict['timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')
        doc_dict['timestamp'] = timestamp_string
        print(timestamp_string)
    data.append(doc_dict)
    print("added question ",doc_dict.get('id'))

# Write the data to a JSON file
with open('questions.json', 'w') as f:
    json.dump(data, f)
