import PyPDF2
import re
import json

pdf_file = open('input.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Extract text from pages
pages = pdf_reader.pages[55:70]
text = ""
for page in pages:
    text += page.extract_text()

# Use regular expressions to extract the questions and options
pattern = r'(\d+\.\s.*?)(?=\d+\.\s|\Z)'
matches = re.findall(pattern, text, flags=re.DOTALL)
# Split the matches into questions and options for each language
questions = {}
for match in matches:
    # Split the match into question number, language, and content
    # q_num, question, options = re.findall(r'(\d+)\.\s+(.*?(?<!\n))(?:\n(?!\Z))?((?:.+\n)*)', match)[0]
    result = re.findall(r'(\d+)\.\s+([^:]+):\s*\n*\s*((?:.+\n*)*)', match)
    
    if not result:
        continue
    q_num, question, options = result[0]
    # Split the content into options'\s*\(?\w\)\s(.+?)(?=\n\(?\w\)|\Z|\n\w\))'
    option_list = re.findall(r'\s*(?P<label>\(?\b\w\)?\s*)\s*(?P<text>.+?)\s*(?=\n\s*\(?\w\)|\Z)', options, flags=re.DOTALL)
    options_dict = []
    for i, option_match in enumerate(option_list):
        option = option_match[1].replace('\n', '').replace('\x00', 'ti')
        is_correct = option_match[0].startswith('(')
        option_dict = {'id': i+1, 'text': option, 'isCorrect': is_correct}
        options_dict.append(option_dict)

    # Initialize the question if it doesn't exist yet
    if q_num not in questions:
        questions[q_num] = {"image":""}
    question = question.replace('\n', '').replace('\u0000','ti')
    if "kinyarwanda" not in questions[q_num]:
        questions[q_num]["kinyarwanda"]={"question":question,"option":options_dict}
    elif "english" not in questions[q_num]:
        questions[q_num]["english"]={"question":question,"option":options_dict}
    elif "french" not in questions[q_num]:
        questions[q_num]["french"]={"question":question,"option":options_dict}
        

# Convert the questions and options to JSON
result = json.dumps(questions, ensure_ascii=False, indent=4)

# Write the JSON to the file
with open('data.json', 'w', encoding='utf-8') as file:
    file.write(result)
