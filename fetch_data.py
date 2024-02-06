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
        course_info = (f"{course['course']['session'].lower()}_"
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

    return {
        "title": thread_info['title'],
        "category": thread_info['category'],
        "question": thread_info['content'],
        "comments": [content['content'] for content in thread_info['comments']],
        "answers": [answer['content'] for answer in thread_info['answers']],
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

# # Process threads for all NLP courses and save the data to a file qac.txt
async def main():
    num_questions = 0

    for course_id, course_info in NLP_courses.items():
        qa_dict = await retrieve_and_process_threads(course_id)
        num_questions += len(qa_dict)
        file_name = f"{course_info}.json"
        with open(file_name, "w") as file:
            json.dump(qa_dict, file, indent=4)
        print(f"Processed course {course_id}")

    print(f"Total of {num_questions} questions were fetched from NLP courses")

asyncio.run(main())

