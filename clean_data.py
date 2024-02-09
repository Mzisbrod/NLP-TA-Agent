import json
import re
import unicodedata
import glob
import os

# Remove html tags and unicode punctuation from string
def clean(text):
    # Normalize Unicode characters to their closest ASCII equivalent
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)

    # Fix missing spaces after punctuation
    text = re.sub(r'([,.!?])([^\s])', r'\1 \2', text)

    return text

def clean_jsonl_file(file_path):
    cleaned_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            entry = json.loads(line)
            # Assuming entry is a dictionary like before
            if 'question' in entry:
                entry['question'] = clean(entry['question'])
            if 'comments' in entry:
                entry['comments'] = [clean(comment) for comment in entry['comments']]
            if 'answers' in entry:
                entry['answers'] = [clean(answer) for answer in entry['answers']]
            cleaned_lines.append(json.dumps(entry))

    cleaned_file_path = file_path.replace('.jsonl', '_cleaned.jsonl')
    with open(cleaned_file_path, 'w', encoding='utf-8') as file:
        for line in cleaned_lines:
            file.write(line + '\n')

# List all JSON Lines files in EdStem Data directory
jsonl_files = glob.glob(os.path.join('EdStem Data', '*.jsonl'))

for jsonl_file in jsonl_files:
    clean_jsonl_file(jsonl_file)
    print(f"Processed and cleaned {jsonl_file}")