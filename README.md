# NLP TA Agent

The NLP TA Agent is designed to streamline the process of managing and responding to student inquiries in Natural Language Processing (NLP) courses.

Utilizing the EdStem API, this tool uses NLP course data and fetches threads, questions and answers from all previous NLP courses. Then, it processes the text, and organizes the data for easy access and analysis.

This project aims to assist TAs and instructors in efficiently monitoring and participating in course discussions, identifying frequently asked questions, and enhancing the overall learning experience.

## Features

- **Thread Fetching**: Automatically retrieves discussion threads from all user's NLP courses on EdStem.
- **Content Cleaning**: Cleans and normalizes the text content of questions, answers, and comments to remove HTML tags and handle Unicode punctuation.
- **TBD**
- **TBD**

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6+
- Access to EdStem API
- Required Python packages: `requests`, `re`, `json`, `asyncio`, `unicodedata`

### Installation

1. Clone the repository to your local machine: `git clone https://github.com/yourusername/nlp-ta-agent.git`
2. Navigate to the project directory: `cd nlp-ta-agent`
3. Install the required Python packages: `pip install -r requirements.txt`

### Usage
1. Configure the '.env' file with your EdStem API token (`https://edstem.org/us/settings/api-tokens`)
2. Run the script to fetch and process data: `python nlp_ta_agent.py`
3. Check the generated `qa_list_cleaned.json` for the processed course data.

### License
This project is licensed under the MIT license

## Acknowledgements
- Thanks to EdStem for providing the API.
- Thanks to Prof. Daniel Bauer for supporting this project.
- Inspired by the needs of NLP students and instructors for better engagement and support.

