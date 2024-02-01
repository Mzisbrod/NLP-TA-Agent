import json # json processing
import re # regular expressions
import unicodedata

# Remove html tags and unicode punctuation from string
def clean(text):
    # Normalize Unicode characters to their closest ASCII equivalent
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)

    # Fix missing spaces after punctuation
    text = re.sub(r'([,.!?])([^\s])', r'\1 \2', text)

    return text

with open("qa_list.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

for entry in data.values():
    entry['question'] = clean(entry['question'])
    entry['answers'] = [clean(answer) for answer in entry['answers']]

with open("qa_list_cleaned.json", 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)