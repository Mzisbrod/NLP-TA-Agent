from openai import OpenAI
import os
from dotenv import load_dotenv
import textwrap
from datasets import load_dataset

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_response(question):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "system","content": "You're a teaching assistant for Natural Language Processing"
                                               "You provide short answers to a student's question, up to 100 words"
                                               "You can't give away answers to homework assignments or exams but only"
                                               "give hints"},
            {"role": "user", "content": question}]
    )
    wrapped_text = textwrap.fill(completion.choices[0].message.content, width=80)  # Wrap text at 80 characters
    return wrapped_text

question = input("Please ask me a question: ")
print("Answer:", get_response(question))
