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
        if re.search(re.escape(ue), re.escape(text), re.IGNORECASE):
            return ue

    # Default to "Syllabus" if none of the above conditions are met
    return "Syllabus"

def merge_json_files(file_paths):
    dict = {} # dictionary with keys=context, values=list of source-target pairs
    for file_path in file_paths:
        match = re.search(r'/([^/]+)_cleaned\.json$', file_path)
        context_file = match.group(1)

        with open(f'course_data/contexts_{context_file}.json', 'r', encoding='utf-8') as contexts_file:
            contexts = json.load(contexts_file)
            for entry in contexts:
                if entry not in dict.keys():
                    dict[entry] = []

        with open(file_path, 'r', encoding='utf-8') as posts_file:
            posts = json.load(posts_file)
            for post in posts:
                context = check_context(post)
                syllabus_key = next(key for key in dict if "Syllabus" in key)
                found_key = next((key for key in dict if context in key), syllabus_key)
                dict[found_key].append(post)

        print(f"Processed file: {file_path}")

    with open('merged_data.json', 'w', encoding='utf-8') as output_file:
        dict_list = []
        for key, values in dict.items():
            inner_dict = {'context': key, 'statements': values}
            dict_list.append(inner_dict)
        json.dump(dict_list, output_file, indent=4)


# List all JSON file paths in Edstem Data directory
file_paths = glob.glob(os.path.join('edstem_data', '*_cleaned.json'))
merge_json_files(file_paths)
#
# for file in file_paths:
#     merge_json_files(file)
# merge_json_files("edstem_data/fall2023_cleaned.json")