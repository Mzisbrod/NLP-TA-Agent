import json
from txtinstruct.models import Instructor

# Load the JSON data
with open("Course_Data/hw1.json", encoding="utf-8") as file:
    data1 = json.load(file)

with open("Course_Data/hw2.json", encoding="utf-8") as file:
    data2 = json.load(file)

data = data1 + data2

# Initialize the Instructor
instructor = Instructor()

# Call the Instructor with appropriate arguments
model, tokenizer = instructor(
    base="google/flan-t5-small",  # Base model or model path
    data=data,  # Instruction-tuning dataset loaded from the JSON file
    task="sequence-sequence",  # Model task
    # Optional: specify a custom prompt template if necessary
    # prompt="Custom prompt template here",
    learning_rate=1e-3,
    per_device_train_batch_size=8,
    gradient_accumulation_steps=128//8,
    num_train_epochs=3,
    logging_steps=100,
)
