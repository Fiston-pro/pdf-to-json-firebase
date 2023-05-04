import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./firebaseSecret.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

questions_ref = db.collection('questions')
docs = questions_ref.get()

for doc in docs:
    doc_dict = doc.to_dict()
    
    # Check if options have incremental ids from 1 to 4
    for lang_key in ['kinyarwanda', 'french', 'english']:
        if 'options' in doc_dict[lang_key]:
            option_ids = [option['id'] for option in doc_dict[lang_key]['options']]
            if set(option_ids) == set([0, 1, 2, 3]):
                for option in doc_dict[lang_key]['options']:
                    option['id'] += 1
                questions_ref.document(doc.id).set(doc_dict)
                print('Updated options for question with id: ' + doc.id+ ' in ' + lang_key)
