from edapi import EdAPI
import re
import json
import time

# Initialize Ed API
ed = EdAPI()
ed.login()

# Retrieve user information
user_info = ed.get_user_info()
NLP_courses = [course['course']['id'] for course in user_info.get('courses', []) if
               course['course']['name'] == 'Natural Language Processing']
NLP_courses.sort()


def clean(str):
    return re.sub(r'<[^>]*>', '', str)


def retrieve_threads(course_id):
    all_threads = []
    offset = 0

    while True:
        threads = ed.list_threads(course_id=course_id, limit=100, offset=offset)
        if not threads:
            break
        all_threads.extend(threads)
        offset += 100

        print(f"Fetched {len(all_threads)} threads from course {course_id} so far..")

    return all_threads

def process_threads(threads):
    qac_list = []
    processed_threads = 0
    total_threads = len(threads)
    for thread in threads:
        qac_dict = {"question": clean(thread['content']), "answers": [], "comments": []}

        time.sleep(1) # Pause to avoid rate limit
        thread_info = ed.get_thread(thread['id'])

        for answer in thread_info["answers"]:
            qac_dict["answers"].append(clean(answer["content"]))
        for comment in thread_info["comments"]:
            qac_dict["comments"].append(clean(comment["content"]))

        qac_list.append(qac_dict)
        processed_threads += 1
    return qac_list


all_qac = []
for course_id in NLP_courses:
    threads = retrieve_threads(course_id)
    all_qac.extend(process_threads(threads))
    print(f"Processed course {course_id}")

with open("qac.txt", "w") as file:
    for qac in all_qac:
        file.write(json.dumps(qac, indent=4) + "\n")
