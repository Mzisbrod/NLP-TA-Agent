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
9. The follwing snippet is an example usage:
    ```
    # Testing
    from txtai.pipeline import Extractor
    from txtai.pipeline import Sequences

    # Load statement generation model

    def prompt(query):
        template = ("Answer the following question using only the context below. "
                    "Say 'I don't have data on that' when the question can't be answered.\n"
                    f"Question: {query}\n"
                    "Context: The assignment focuses on n-gram extraction/counting. "
                    "For Part 1, `get_ngrams` needs to generate padded n-grams from strings. "
                    "Part 2 involves counting n-grams within two datasets, primarily the Brown corpus, "
                    "using a lexicon for unseen words, marked as 'UNK'. The `TrigramModel` is initialized "
                    "with a corpus file for lexicon collection and n-gram counting. `count_ngrams` updates "
                    "frequency dictionaries for unigrams, bigrams, and trigrams. The process accommodates unseen words "
                    "and efficient reading, with model testing done via `brown_test.txt` for perplexity evaluation.")
        return template

    question = ("Homework 1 Question 6. Do we need to count the word 1 more than each sentence "
                "when computing perplexity? Because I think there will be a hiding STOP "
                "for each sentence. So the total word tokens is the words in document plus "
                "number of sentences. Am I understanding this correctly?")

    extractor = Extractor(embeddings, Sequences((model, tokenizer)))
    extractor([{"query": f"{question}", "question": prompt(f"{question}")}])
    ```


### License
This project is licensed under the MIT license

## Acknowledgements and credits
- Thanks to  EdStem for providing the token API
- Credit for fetching EdStem data: `https://github.com/smartspot2/edapi/tree/master`
- Credit for Instruction Tuning inspiration: `https://medium.com/neuml/instruction-tune-models-using-your-own-data-with-txtinstruct-3008d8c8d025`
- Thanks to Prof. Daniel Bauer for supporting this project
- Inspired by the needs of NLP students and instructors for better engagement and support

