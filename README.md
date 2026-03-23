# RAG Translation Backend

A Python backend developed for the Translated Junior ML Engineer technical test.

The application exposes a REST API that stores translation pairs, retrieves the most relevant examples for a translation request, builds a Retrieval-Augmented Generation (RAG) prompt, and provides an advanced stammering detection endpoint.

## Features

- Store translation pairs in a local SQLite database
- Retrieve up to 4 similar examples using TF-IDF + cosine similarity
- Build a translation prompt enriched with retrieved examples
- Detect translation stammering using a local heuristic algorithm
- Support reverse-direction retrieval by reusing stored pairs in the opposite direction
- Run locally or inside a Docker container

## Tech Stack

- **FastAPI** for the REST API
- **SQLite** for persistence
- **scikit-learn** for similarity search
- **Uvicorn** as the ASGI server
- **Docker** for containerization

The implementation is intentionally simple, modular, and easy to run locally.

## Project Structure

```text
app/
  main.py
  db.py
  schemas.py
  repository.py
  retrieval.py
  prompt_builder.py
  stammering.py
  services.py
outputs/
requirements.txt
Dockerfile
README.md
client.py
translation_pairs.jsonl
translation_requests.jsonl
stammering_tests.jsonl
```

## Requirements

- Python 3.11+ recommended


## Setup

Create and activate a virtual environment, then install dependencies.

## Run the Application Locally

Start the API server with:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

## (Optional) Run with Docker

Docker support is included as an additional score booster.

### Build the image

```bash
docker build -t rag-translation-backend .
```

### Run the container

```bash
docker run -p 8000:8000 rag-translation-backend
```

The API will then be available at:

- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

## Captured Outputs

The `outputs/` folder contains the captured outputs produced by running the different steps of `client.py`, as requested in the submission instructions.

It includes the outputs for:

- database population
- prompt generation requests
- stammering detection tests

This allows the evaluator to inspect the application behavior without having to reproduce every step manually.

## Retrieval Strategy

For each translation request:

1. candidate translation pairs are loaded from SQLite
2. both direct and reverse-direction pairs can be used
3. TF-IDF vectors are computed on the source-side sentences
4. cosine similarity is used to rank the candidates
5. the top 4 most relevant examples are added to the generated prompt

This approach is lightweight, effective for a small dataset, and easy to explain.

## Stammering Detection

The advanced endpoint is implemented locally without relying on external stammering detection systems.

The heuristic detects suspicious patterns such as:

- repeated consecutive words
- repeated consecutive n-grams
- abnormally long translated sequences compared to the source
- excessive character elongations not justified by the source sentence

The goal is to keep the solution simple, deterministic, and easy to maintain.

## Design Notes

A few implementation choices were made to keep the project practical and clear:

- **SQLite** was chosen because it is lightweight and sufficient for the scope of the task
- **TF-IDF + cosine similarity** provides a simple and reliable baseline for retrieving similar translation pairs
- **FastAPI** makes the API easy to develop, test, and document
- **services.py** was introduced to keep the orchestration logic separated from the endpoint layer
