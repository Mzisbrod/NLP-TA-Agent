import json
from txtinstruct.models import Instructor
import torch
import os

os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.8'  # Adjust as necessary within the range [0.0, 1.0]

# For CPU
torch.set_default_device('cpu')

# For GPU (if available)
if torch.cuda.is_available():
    torch.set_default_device('cuda')

data = []

# Load all cleaned edstem_data json files
file_path = 'merged_data.json'

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
    per_device_train_batch_size=8, # Changed from 4
    gradient_accumulation_steps=32, # Changed from 128 // 8,
    num_train_epochs=3,
    logging_steps=100,
)

path = "./trained_model"
model.save_pretrained(path)
tokenizer.save_pretrained(path)
