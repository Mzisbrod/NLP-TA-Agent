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

# Given a file path with json files, clean the file and create
# a cleaned version of it
def clean_json_file(file_path):
    cleaned_file_path = file_path.replace('.json', '_cleaned.json')
    with open(file_path, 'r', encoding='utf-8') as input_file, \
         open(cleaned_file_path, 'w', encoding='utf-8') as output_file:
        data = json.load(input_file)
        cleaned_data = []
        for entry in data:
            cleaned_entry = {}
            for key, value in entry.items():
                if isinstance(value, str):
                    cleaned_entry[key] = clean(value)
                elif isinstance(value, list):
                    cleaned_entry[key] = [clean(item) for item in value]
                else:
                    cleaned_entry[key] = value
            cleaned_data.append(cleaned_entry)
        json.dump(cleaned_data, output_file, indent=4)

    print(f"Processed and cleaned {file_path}")

# List all JSON files in Edstem Data directory
json_files = glob.glob(os.path.join('Edstem_Data', '*.json'))

for json_file in json_files:
    clean_json_file(json_file)