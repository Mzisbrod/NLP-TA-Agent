# Merges the data of HWs, Ungraded Exercises, and Syllabus with fetched EdStem posts
import json
import glob
import os
import re

def check_context(source_target):
    text = source_target["source"] + " " + source_target["target"] # Concatenated post

    # Check for HW or Homework
    hw_match = re.search(r'(HW|Homework)[\s-]*(\d+)', text, re.IGNORECASE)
    if hw_match:
        return f"Homework {hw_match.group(2)}"

    # Else, define a mapping of keywords to their respective exercise types for Ungraded Exercises
    ue_list = ['Naive', 'n-gram', 'HMM', 'CKY', 'Transition', 'Linear Models', 'AMR', 'IBM', 'Graph', 'PCFGs', 'Viterbi']

    # Check for "Ungraded Exercise" and try to match one of the specified types
    for ue in ue_list:
        # if re.search(r'Ungraded Exercise(?: -)?[ :]+.*?\b' + re.escape(ue) + r'\b', text, re.IGNORECASE):
        #     return ue
        if re.search(re.escape(ue), re.escape(text), re.IGNORECASE):
            return ue

    # Default to "Syllabus" if none of the above conditions are met
    return "Syllabus"

def merge_json_files(file_path):
    match = re.search(r'/([^/]+)_cleaned\.json$', file_path)
    context_file = match.group(1)
    merged_file_path = file_path.replace('_cleaned.json', '_complete.json')
    dict = {}

    with open(f'contexts_{context_file}.json', 'r', encoding='utf-8') as contexts_file:
        contexts = json.load(contexts_file)
        for entry in contexts:
            dict[entry] = []

    with open(file_path, 'r', encoding='utf-8') as posts_file:
        posts = json.load(posts_file)
        for post in posts:
            context = check_context(post)
            syllabus_key = next(key for key in dict if "Syllabus" in key)
            found_key = next((key for key in dict if context in key), syllabus_key)
            dict[found_key].append(post)

    print(len(dict[syllabus_key]))
    with open(merged_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(dict, output_file, indent=4)

    print(f"Processed and merged {file_path}")
#
# # List all JSON file paths in Edstem Data directory
# file_paths = glob.glob(os.path.join('edstem_data', '*.json'))
#
# for file in file_paths:
#     merge_json_files(file)
merge_json_files("edstem_data/fall2023_cleaned.json")