import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('./firebaseSecret.json')
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()

# Get the number of documents in the "questions" collection
questions_ref = db.collection('questions')
num_docs = len(list(questions_ref.get()))
print(f"Number of documents in 'questions' collection: {num_docs}")

# Get the number of objects in the "questions.json" file
backUpFile = 'questionsBackup1.json'
with open(backUpFile, 'r') as f:
    data = json.load(f)
num_objs = len(data)
print(f"Number of objects in backup file: {num_objs}")
