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

# get all documents from the "users" collection
users_ref = db.collection('users')
users = users_ref.get()

# iterate over each user document
for user in users:
    user_ref = users_ref.document(user.id)

    # read the "doneQuestions" field and get the count of elements in the array
    done_questions = user.get('doneQuestions')
    num_done_questions = len(done_questions)

    # update the document with the new "questionsDoneCorrectly" value and remove "doneQuestions"
    user_ref.update({
        'questionsDoneCorrectly': num_done_questions
    })
    user_ref.update({
        'doneQuestions': firestore.DELETE_FIELD
    })

    print(f'Updated user {user.id} with {num_done_questions} done questions')


print('Done updating documents')
