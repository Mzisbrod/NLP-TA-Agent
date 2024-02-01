from edapi import EdAPI
import json
import asyncio

# Initialize Ed API & log in
ed = EdAPI()
ed.login()

# Retrieve user information and create dictionary of NLP courses IDs
user_info = ed.get_user_info()
NLP_courses = {}
for course in user_info.get('courses', []):
    if course['course']['name'] == 'Natural Language Processing':
        course_info = (f"NLP {course['course']['session']} "
                       f"{course['course']['year']}")
        NLP_courses[course['course']['id']] = course_info

""" Get thread information using thread ID and handle rate limits by catching
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

""" Process individual threads by retrieving first and then
    assign answers to available answers/comments of each thread """
async def process_thread(thread):
    thread_info = await retrieve_thread_info(thread['id'])
    answers_or_comments = thread_info['answers'] if thread_info['answers'] \
        else thread_info['comments']
    return {
        "question": thread['content'],
        "answers": [answer['content'] for answer in answers_or_comments]
    }

""" Given thread dictionary, return True if it was made by a student:
    None if it's by an anonymous person """
def valid(thread):
    return (thread.get('user') is None) or (thread.get('user')['course_role'] == 'student')

# Retrieve all threads for a course and process them
async def retrieve_and_process_threads(course_id):
    all_threads = []
    offset = 0
    total_threads_fetched = 0

    while True:
        try:
            threads = ed.list_threads(course_id=course_id, limit=100, offset=offset)
            if not threads:
                break
            filtered_threads = []
            for thread in threads:
                if valid(thread): # Filters out non-student posts
                    filtered_threads.append(thread)

            all_threads.extend(filtered_threads)
            offset += 100
            total_threads_fetched += len(threads)
            print(f"Fetched {total_threads_fetched} threads from "
                  f"course {course_id} so far..")
        except Exception as e:
            if 'rate_limit' in str(e):
                print(f"Rate limit reached. Waiting before retrying..")
                await asyncio.sleep(1)
            else:
                raise # Re-raise other exceptions

    qa_dict = {}
    thread_counter = 0 # Key of each thread
    for thread in all_threads:
        processed_thread = await process_thread(thread)
        if processed_thread is not None:
            qa_dict[thread_counter] = processed_thread
            thread_counter += 1

    return qa_dict

# Process threads for all NLP courses and save the data to a file qac.txt
async def main():
    all_qa = {}

    for course_id in NLP_courses.keys():
        qa_dict = await retrieve_and_process_threads(course_id)
        all_qa.update(qa_dict) # Merge the dictionaries
        print(f"Processed course {course_id}")

    with open("qa_list.json", "w") as file:
        json.dump(all_qa, file, indent=4)

    print(f"Total of {len(all_qa)} questions were fetched from NLP courses")

asyncio.run(main())

