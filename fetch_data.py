from edapi import EdAPI
import re
import json

# Initialize Ed API
ed = EdAPI()
# Authenticate user through ED_API_TOKEN environment variable
ed.login()

# Retrieve user information
user_info = ed.get_user_info()
# List to extract all NLP courses' IDs
NLP_courses = []

# Get list of all courses with their EdStem ID
for course in user_info.get('courses'):
    # print(f"Name: {course['course']['name']}, "
    #       f"Year: {course['course']['year']}, "
    #       f"Session: {course['course']['session']}, "
    #       f"ID: {course['course']['id']}")
    if course['course']['name'] == 'Natural Language Processing': # Extract NLP
        NLP_courses.append(course['course']['id'])

NLP_courses.sort() # Sorts IDs from older to newer NLP course

# Method to remove everything within <..> tags of given string
def clean(str):
    return re.sub(r'<[^>]*>', '', str)

file = open("qac.txt", "w")
# Fetch list of course's threads
threads = ed.list_threads(course_id=NLP_courses[0], limit=100)

# For each of the threads, create a qac (question-answers-comments) dictionary
for thread in threads:
    qac_dict = {"question": clean(thread['content'])} # Add question as key with value string
    answers = []
    comments = []
    thread_info = ed.get_thread(thread['id'])
    for answer in thread_info["answers"]:
        answers.append(clean(answer["content"]))
    qac_dict["answers"] = answers
    for comment in thread_info["comments"]:
        comments.append(clean(comment["content"]))
    qac_dict["comments"] = comments
    file.writelines(json.dumps(qac_dict, indent=4) + "\n") # Write dictionary to file
