# Merges the data of HWs, Ungraded Exercises, and Syllabus with fetched EdStem posts
import json
import glob
import os
import re

def check_context(text):
    # text = pair["source"] + " " + pair["target"]
    # Regular expression to find 'HW' or 'Homework' followed by optional whitespace and a number within the range 1-5
    pattern = re.compile(r'\b(?:HW|Homework)\s*(\d+)', re.IGNORECASE)

    # Search the text for the pattern
    match = pattern.search(text)

    if match:
        # If a match is found, return the number (converted to int)
        return int(match.group(1))

    # Return None if no match is found
    return None

# # Given a file path with json files, clean the file and create a cleaned version of it
# def merge_json_files(file_path):
#     merged_file_path = file_path.replace('_cleaned.json', 'merged.json')
#     merged_data = []
#     with open(file_path, 'r', encoding='utf-8') as input_file:
#         data = json.load(input_file)
#         for pair in data:
#
#
#     with open(merged_file_path, 'w', encoding='utf-8') as output_file:
#         json.dump(merged_data, output_file, indent=4)
#
#     print(f"Processed and merged {file_path}")
#
# # List all JSON file paths in Edstem Data directory
# file_paths = glob.glob(os.path.join('edstem_data', '*.json'))
#
# for file in file_paths:
#     merge_json_files(file)