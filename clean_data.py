import json
import re
import unicodedata
import glob

# Remove html tags and unicode punctuation from string
def clean(text):
    # Normalize Unicode characters to their closest ASCII equivalent
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)

    # Fix missing spaces after punctuation
    text = re.sub(r'([,.!?])([^\s])', r'\1 \2', text)

    return text

# with open("qa_list.json", 'r', encoding='utf-8') as file:
#     data = json.load(file)
#
# count = 0
# for entry in data.values():
#     entry['question'] = clean(entry['question'])
#     entry['answers'] = [clean(answer) for answer in entry['answers']]
#
# with open("qa_list_cleaned.json", 'w', encoding='utf-8') as file:
#     json.dump(data, file, indent=4)

def clean_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for entry in data.values():
        entry['question'] = clean(entry['question'])
        entry['comments'] = [clean(comment) for comment in entry['comments']]
        entry['answers'] = [clean(answer) for answer in entry['answers']]

    cleaned_file_path = file_path.replace('.json', '_cleaned.json')
    with open(cleaned_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# List all JSON files in the current directory
json_files = glob.glob('*.json')

for json_file in json_files:
    clean_json_file(json_file)
    print(f"Processed and cleaned {json_file}")