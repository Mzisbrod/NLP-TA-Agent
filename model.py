# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# import textwrap
from datasets import load_dataset, Dataset
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer

# Specifies multiple file paths for all training files
data_files = {
    'train': ['EdStem_Data/summer_2023_cleaned.jsonl',
              'EdStem_Data/fall_2023_cleaned.jsonl',
              'EdStem_Data/spring_2024_cleaned.jsonl',
              'Old_Material/hw1.jsonl']
}

# Load the datasets
dataset = load_dataset('json', data_files=data_files, split='train')
data = [item['title'] + '' + item['question'] + '' + item['answer'] for item in dataset]

# Splitting the data
train_temp, test_data = train_test_split(data, test_size=0.3, random_state=42)
train_data, valid_data = train_test_split(train_temp, test_size=0.2143, random_state=42)

# Converting split data into Huggingface Datasets
train_dataset = Dataset.from_dict({'text': train_data})
valid_dataset = Dataset.from_dict({'text': valid_data})
test_dataset = Dataset.from_dict({'text': test_data})

# Tokenize the datasets
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')

def tokenize_function(examples):
    return tokenizer(examples['text'], padding=True, truncation=True, max_length=512)

tokenized_train_dataset = train_dataset.map(tokenize_function, batched=True)
tokenized_valid_dataset = valid_dataset.map(tokenize_function, batched=True)
tokenized_test_dataset = test_dataset.map(tokenize_function, batched=True)

# Disable the token type IDs for GPT model training
tokenized_train_dataset = tokenized_train_dataset.remove_columns(["token_type_ids"])
tokenized_valid_dataset = tokenized_valid_dataset.remove_columns(["token_type_ids"])
tokenized_test_dataset = tokenized_test_dataset.remove_columns(["token_type_ids"])

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4, # Might have to adjust this
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Initialize the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_valid_dataset,
)

# Train the model
trainer.train()

# Evaluate the model
trainer.evaluate(tokenized_test_dataset)






# load_dotenv()
#
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
#
# def get_response(question):
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo-1106",
#         messages=[{"role": "system","content": "You're a teaching assistant for Natural Language Processing"
#                                                "You provide short answers to a student's question, up to 100 words"
#                                                "You can't give away answers to homework assignments or exams but only"
#                                                "give hints"},
#             {"role": "user", "content": question}]
#     )
#     wrapped_text = textwrap.fill(completion.choices[0].message.content, width=80)  # Wrap text at 80 characters
#     return wrapped_text
#
# question = input("Please ask me a question: ")
# print("Answer:", get_response(question))
