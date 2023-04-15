import json

# Read data from questions.json file
with open('questionsBackup1.json', 'r') as f:
    data = json.load(f)

# Extract IDs from each document
ids = [doc['id'] for doc in data]

# Define the range of numbers to check
start_number = 1
end_number = 210

# Check which IDs are missing from the range
missing_ids = []
for i in range(start_number, end_number + 1):
    if str(i) not in ids:
        missing_ids.append(i)

# Print the missing IDs
print('Missing IDs:')
print(missing_ids)
