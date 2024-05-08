# NLP TA Agent

The NLP TA Agent is designed to streamline the process of managing and responding to student inquiries in Natural Language Processing (NLP) courses.

Utilizing the EdStem API, this tool uses NLP course data and fetches threads, questions and answers from all previous NLP courses. Then, it processes the text, and organizes the data for easy access and analysis.

This project aims to assist TAs and instructors in efficiently monitoring and participating in course discussions, identifying frequently asked questions, and enhancing the overall learning experience.

## Features

- **Thread Fetching**: Automatically retrieves discussion threads from all user's NLP courses on EdStem.
- **Content Cleaning**: Cleans and normalizes the text content of questions, answers, and comments to remove HTML tags and handle Unicode punctuation.
- **Text Completion**: The model learns course material by providing output to any input from it.
- **Instruction Tuning**: Model is further trained on previous EdStem posts and comments.

## Getting Started

These instructions will get you a copy of the project up and running on virtual machine for development and testing purposes.

### Prerequisites

- Python 3.6+
- Access to EdStem API
- Python packages: `sentencepiece, txtinstruct, transformers, torch, os`

### Installation

1. Clone the repository to your local machine: `git clone https://github.com/<yourusername>/nlp-ta-agent.git`
2. Navigate to the project directory: `cd nlp-ta-agent`
3. Install any necessary Python packages

### Usage
1. Configure the `.env` file with your EdStem API token (`https://edstem.org/us/settings/api-tokens`)
2. Fetch EdStem data by running `python fetch_data.py` (saved in `/edstem_data` directory)
3. Prepare the data for training by running `python clean_data.py` (saved in `/edstem_data` directory)
4. Merge the data fetched from all courses by running `python merge_data.py`. Now `merged_data.json` conatains all course data fetched from EdStem
5. Prepare course data as JSON file and save in `/course_data`
6. Run the script load and process data: `model.ipynb`
7. Check the generated output to chosen question
8. Generated models are saved in the following directories: `/trained_completion_model, /trained_model`

### License
This project is licensed under the MIT license

## Acknowledgements
- Thanks to EdStem for providing the API.
- Thanks to Prof. Daniel Bauer for supporting this project.
- Inspired by the needs of NLP students and instructors for better engagement and support.

