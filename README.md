# English to Vietnamese Translation API

## Student Information

- Full name: YOUR NAME
- Student ID: YOUR STUDENT ID
- Course: Computational Thinking

## Project Description

This project uses FastAPI to provide an API that translates English text
into Vietnamese using a pretrained Hugging Face model.

The API validates input data and returns translation results in JSON format.

## Model

- Model: Helsinki-NLP/opus-mt-en-vi
- Model page: https://huggingface.co/Helsinki-NLP/opus-mt-en-vi
- Task: English-to-Vietnamese translation
- The model runs on CPU and is loaded once when the application starts.

## Project Structure

```text
translation-api/
├── main.py
├── test_api.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Requirements: Python 3.11 and an Internet connection for the first model download.

Download or clone this repository, then open a terminal in the project folder.

Create a virtual environment:

```powershell
python -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the Application

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app
```

The first startup downloads the model from Hugging Face.
Wait until the application finishes starting.

Interactive API documentation:
http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Return an introduction to the API |
| GET | /health | Check whether the model is ready |
| POST | /predict | Translate English text into Vietnamese |

### Translation Example

Send a POST request to `http://127.0.0.1:8000/predict`.

Request body:

```json
{
  "text": "I am a student."
}
```

Example response:

```json
{
  "input": "I am a student.",
  "translation": "Tôi là một học sinh.",
  "model": "Helsinki-NLP/opus-mt-en-vi"
}
```

Example using Python:

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={"text": "I am a student."},
    timeout=120,
)

print(response.status_code)
print(response.json())
```

### Input Validation and Errors

- `text` must be a string containing 1–500 characters.
- Empty or whitespace-only text is rejected.
- Invalid input returns HTTP 422.
- An unavailable model returns HTTP 503 while the application is serving.
- Translation failures return HTTP 500.

## Run API Tests

Keep the API server running and open another terminal:

```powershell
.\.venv\Scripts\python.exe test_api.py
```

The tests check the introduction endpoint, model readiness,
two translation inputs, and invalid input cases.

A successful run ends with:

```text
All tests passed!
```

## Limitations

- The model is intended for English-to-Vietnamese translation.
- Translation quality may vary depending on the input.
- The API does not automatically verify the input language.
- If the model cannot load during startup, the application cannot start.

## Demonstration Video

TODO: Add the demonstration video link before submission.