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

def clean_text_or_list(input):
    if isinstance(input, list):
        return [clean(item) for item in input]
    return clean(input)

# Given a file path with json files, clean the file and create a cleaned version of it
def clean_json_file(file_path):
    cleaned_file_path = file_path.replace('.json', '_cleaned.json')
    cleaned_data = []
    with open(file_path, 'r', encoding='utf-8') as input_file:
        data = json.load(input_file)
        for entry in data:
            cleaned_context = clean(entry["context"])
            cleaned_statements = []
            for statement in entry["statements"]:
                cleaned_source = clean_text_or_list(statement["source"])
                cleaned_target = clean_text_or_list(statement["target"])
                cleaned_statements.append({"source": cleaned_source,
                                           "target": cleaned_target})
            cleaned_data.append({"context": cleaned_context, "statements": cleaned_statements})

    with open(cleaned_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(cleaned_data, output_file, indent=4)

    print(f"Processed and cleaned {file_path}")

# List all JSON file paths in Edstem Data directory
file_paths = glob.glob(os.path.join('edstem_data', '*.json'))

for file in file_paths:
    clean_json_file(file)
