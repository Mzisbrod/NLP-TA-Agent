import json
from txtinstruct.models import Instructor
import glob
import os

data = []

# Load all cleaned edstem_data json files
file_paths = glob.glob(os.path.join('course_data', '*.json')) # glob.glob(os.path.join('edstem_data', '*_cleaned.json'))

for file_path in file_paths:
    with open(file_path, encoding="utf-8") as f:
        data += json.load(f)

# Initialize the Instructor
instructor = Instructor()

# Call the Instructor with appropriate arguments
model, tokenizer = instructor(
    base="google/flan-t5-small",  # Base model or model path
    data=data,  # Instruction-tuning dataset loaded from the JSON file
    task="sequence-sequence",  # Model task
    # Optional: specify a custom prompt template if necessary
    # prompt=
    learning_rate=1e-3,
    per_device_train_batch_size=8,
    gradient_accumulation_steps=128 // 8,
    num_train_epochs=3,
    logging_steps=100,
)
