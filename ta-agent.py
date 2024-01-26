from openai import OpenAI
import textwrap

client = OpenAI(api_key="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")

def generate_response(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"You are a Natural Language Processing Teaching Assistant."
                        f"Respond to the student's question: '{question},'"
                        f"making sure not to give away answers to homework questions in full or"
                        f"give away answers to exam questions. Answers to material"
                        f"is accepted. Provide short answers"},
        ]
    )
    return response.choices[0].message


if __name__ == "__main__":
    question = input("Please ask a question: ")
    print("Answer:", end=' ')
    print(textwrap.fill(generate_response(question).content))
