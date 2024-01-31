# from edapi import EdAPI
# import re
# import json
# import time
#
# # Initialize Ed API
# ed = EdAPI()
# ed.login()
#
# # Retrieve user information
# user_info = ed.get_user_info()
# NLP_courses = [course['course']['id'] for course in user_info.get('courses', []) if
#                course['course']['name'] == 'Natural Language Processing']
# NLP_courses.sort()
#
#
# def clean(str):
#     return re.sub(r'<[^>]*>', '', str)
#
#
# def retrieve_threads(course_id):
#     all_threads = []
#     offset = 0
#
#     while True:
#         threads = ed.list_threads(course_id=course_id, limit=100, offset=offset)
#         if not threads:
#             break
#         all_threads.extend(threads)
#         offset += 100
#
#         print(f"Fetched {len(all_threads)} threads from course {course_id} so far..")
#
#     return all_threads
#
# def process_threads(threads):
#     qac_list = []
#     processed_threads = 0
#     total_threads = len(threads)
#     for thread in threads:
#         qac_dict = {"question": clean(thread['content']), "answers": [], "comments": []}
#
#         time.sleep(1) # Pause to avoid rate limit
#         thread_info = ed.get_thread(thread['id'])
#
#         for answer in thread_info["answers"]:
#             qac_dict["answers"].append(clean(answer["content"]))
#         for comment in thread_info["comments"]:
#             qac_dict["comments"].append(clean(comment["content"]))
#
#         qac_list.append(qac_dict)
#         processed_threads += 1
#     return qac_list
#
#
# all_qac = []
# for course_id in NLP_courses:
#     threads = retrieve_threads(course_id)
#     all_qac.extend(process_threads(threads))
#     print(f"Processed course {course_id}")
#
# with open("qac.txt", "w") as file:
#     for qac in all_qac:
#         file.write(json.dumps(qac, indent=4) + "\n")

from edapi import EdAPI # API access
import re # regular expressions
import json # JSON processing
import asyncio # asynchronous programming

# Initialize Ed API & log in
ed = EdAPI()
ed.login()

# Retrieve user information and create list of NLP courses' IDs
user_info = ed.get_user_info()
NLP_courses = sorted([course['course']['id'] for course in user_info.get('courses', []) if
                      course['course']['name'] == 'Natural Language Processing'])

# Remove HTML tags from string
def clean(text):
    return re.sub(r'<[^>]*>', '', text)

""" Fetch thread information using thread ID and handle rate limits by catching
    exceptions and retrying after a pause """
async def retrieve_thread_info(thread_id):
    try:
        return ed.get_thread(thread_id)
    except Exception as e:  # Catching general exception
        if 'rate_limit' in str(e):  # Check if it's a rate limit issue
            await asyncio.sleep(1)
            return await retrieve_thread_info(thread_id)
        else:
            print("An error occurred: ", e) # Print other error message
            raise

""" Process individual threads by retrieving first and then cleaning the content
    of each thread into question, answers, and comments """
async def process_thread(thread):
    thread_info = await retrieve_thread_info(thread['id'])
    return {
        "question": clean(thread['content']),
        "answers": [clean(answer["content"]) for answer in thread_info["answers"]],
        "comments": [clean(comment["content"]) for comment in thread_info["comments"]]
    }

# Retrieve all threads for a course and process them
async def retrieve_and_process_threads(course_id):
    all_threads = []
    offset = 0
    total_threads_fetched = 0

    while True:
        threads = ed.list_threads(course_id=course_id, limit=100, offset=offset)
        if not threads:
            break
        all_threads.extend(threads)
        offset += 100
        total_threads_fetched += len(threads)
        print(f"Fetched {total_threads_fetched} threads from course {course_id} so far..")

    qac_list = await asyncio.gather(*(process_thread(thread) for thread in all_threads))
    return qac_list

# Process threads for all NLP courses and save the data to a file qac.txt
async def main():
    all_qac = []
    for course_id in NLP_courses:
        qac_list = await retrieve_and_process_threads(course_id)
        all_qac.extend(qac_list)
        print(f"Processed course {course_id}")

    with open("qac.txt", "w") as file:
        for qac in all_qac:
            file.write(json.dumps(qac, indent=4) + "\n")

    print(f"Total of {len(all_qac)} questions were fetched from NLP courses")

asyncio.run(main())

