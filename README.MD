# Wordle API

## Overview

The Wordle API is a FastAPI application that allows users to play a word-guessing game similar to Wordle. It includes features for checking guesses against target words, retrieving daily words, and segmenting words from a given string.

## Features

- **Daily Word Guessing**: Users can guess a daily word.
- **Random Word Guessing**: Users can guess a randomly selected word.
- **Word Segmentation**: Users can segment a string into individual words.
- **Customizable Word Size**: Users can specify the size of the word for guessing.

## Requirements

- Python 3.7 or higher
- FastAPI
- Uvicorn
- Wordninja (for word segmentation)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/wordle-api.git
   cd wordle-api
   ```

2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install the required packages:
```
pip install -r requirements.txt
```

## Running the Application

To run the FastAPI application, use the following command:
```
uvicorn wordle:app --reload
```

The application will be available at http://127.0.0.1:8000.

## API Endpoints
1. Daily Word Guessing
- Endpoint: /daily
- Method: GET
- Parameters:
    - guess (string): Your guess for the daily word.
    - size (int, optional): The size of the word (default is 5).

Example:
```
curl "http://127.0.0.1:8000/daily?guess=plane&size=5"
```

2. Random Word Guessing
- Endpoint: /random
- Method: GET
- Parameters:
- guess (string): Your guess for the random word.
    - size (int, optional): The size of the word (default is 5).
    - seed (int, optional): Random seed for reproducibility.
Example:
```
curl "http://127.0.0.1:8000/random?guess=brake&size=5&seed=42"
```

3. Guess Against a Specific Word
- Endpoint: /word/{word}
- Method: GET
- Parameters:
    - word (string): The target word.
    - guess (string): Your guess for the word.
Example:
```
curl "http://127.0.0.1:8000/word/world?guess=plane"
```

4. Word Segmentation
- Endpoint: /wordseg
- Method: POST
- Body: Form data with a single field text.
Example:
```
curl -X POST "http://127.0.0.1:8000/wordseg" -d "text=worldplanecrane"
```

## Testing the API
You can test the API using tools like Postman or curl. Here are some basic tests you can perform:

Test Daily Word Guess:
```
curl "http://127.0.0.1:8000/daily?guess=plane&size=5"
```
Test Random Word Guess:
```
curl "http://127.0.0.1:8000/random?guess=brake&size=5"
```
Test Word Segmentation:
```
curl -X POST "http://127.0.0.1:8000/wordseg" -d "text=worldplanecrane"
```