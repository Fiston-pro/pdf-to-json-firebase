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
    lang_keys = ['kinyarwanda', 'french', 'english']
    
    # Check if all required keys are present
    if not all(key in doc_dict for key in lang_keys):
        print(f"Missing language key in {doc.id}")
        continue
    
    # Check if all options have unique ids
    for lang_key in lang_keys:
        if 'options' in doc_dict[lang_key]:
            option_ids = set()
            num_correct_options = 0
            for option in doc_dict[lang_key]['options']:
                option_id = option.get('id')
                if option_id is None:
                    print(f"Missing option id in {lang_key} in {doc.id}")
                    continue
                if option_id in option_ids:
                    print(f"Duplicate option id {option_id} in {lang_key} in {doc.id}")
                    continue
                option_ids.add(option_id)
                
                is_correct = option.get('isCorrect', False)
                if is_correct:
                    num_correct_options += 1
            
            if num_correct_options != 1:
                print(f"Invalid number of correct options ({num_correct_options}) in {doc.id} - {lang_key}")
    
    # Check if options have incremental ids from 1 to 4
    for lang_key in lang_keys:
        if 'options' in doc_dict[lang_key]:
            option_ids = [option['id'] for option in doc_dict[lang_key]['options']]
            if set(option_ids) != set([1, 2, 3, 4]) and set(option_ids) != set([0, 1, 2, 3]):
                print(f"Options do not have correct ids in {doc.id} - {lang_key}")
            if len(option_ids) != 4:
                print(f"Options do not have correct number of ids in {doc.id} - {lang_key}")
    
    # Check if all required fields are present in each language dict
    for lang_key in lang_keys:
        lang_dict = doc_dict[lang_key]
        if 'question' not in lang_dict:
            print(f"Missing question field in {doc.id} - {lang_key}")
        if 'options' in lang_dict:
            for option in lang_dict['options']:
                if 'text' not in option:
                    print(f"Missing option text field in {doc.id} - {lang_key}")
        else:
            print(f"Missing options field in {doc.id} - {lang_key}")

    # check if all correct ids are the same in all languages
    correct_ids = ""
    for lang_key in lang_keys:
        if 'options' in doc_dict[lang_key]:
            for option in doc_dict[lang_key]['options']:
                if option['isCorrect'] and (correct_ids == "" or correct_ids == str(option['id'])):
                    correct_ids = str(option['id'])
                elif option['isCorrect']:
                    print(f"Correct ids are not the same in all languages in {doc.id}")
                    break
        else:
            print(f"Missing options field in {doc.id} - {lang_key}")

    for lang_key in lang_keys:
        text = "Uburebure bw'ibinyabiziga"
        if text in doc_dict[lang_key]['question']:
            print(f"Found {doc.id} - {lang_key}")
            print(doc_dict[lang_key]['question'])
    