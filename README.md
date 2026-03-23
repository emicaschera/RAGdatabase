# RAG Translation Backend

A simple Python backend for the Translated Junior ML Engineer test.

## What it does

- stores translation pairs in SQLite
- retrieves up to 4 similar examples with TF-IDF + cosine similarity
- builds a translation prompt for an LLM
- detects translation stammering with a local heuristic algorithm
- supports reverse-direction retrieval by reusing stored pairs in the opposite direction

## Tech choices

- **FastAPI** for the REST API
- **SQLite** for persistence
- **scikit-learn** for similarity search

This keeps the project small, easy to explain, and easy to run.

## Project structure

```text
app/
  main.py
  db.py
  schemas.py
  repository.py
  retrieval.py
  prompt_builder.py
  stammering.py
requirements.txt
Dockerfile
README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## Endpoints

### POST /pairs

Request body:

```json
{
  "source_language": "en",
  "target_language": "it",
  "sentence": "Good morning!",
  "translation": "Buongiorno!"
}
```

Response:

```json
{
  "status": "ok"
}
```

### GET /prompt

Example:

```bash
curl "http://127.0.0.1:8000/prompt?source_language=en&target_language=it&query_sentence=Good%20night"
```

### GET /stammering

Example:

```bash
curl "http://127.0.0.1:8000/stammering?source_sentence=ciao%20ciao&translated_sentence=bye%20bye%20bye%20bye%20bye%20bye%20bye"
```

## How retrieval works

For a given request:

1. all candidate pairs matching the requested direction are loaded from SQLite
2. pairs in the reverse direction are also reused by swapping source and target texts
3. TF-IDF vectors are computed on the candidate source-side sentences
4. cosine similarity is used to rank candidates
5. the top 4 pairs are inserted into the generated prompt

The chosen vectorizer uses character n-grams (`char_wb`, 3 to 5). This works well for short sentences and is robust enough for small datasets without adding too much complexity.

## How stammering detection works

The local algorithm flags suspicious cases such as:

- repeated consecutive words in the translated sentence
- repeated consecutive n-grams such as `is really the` repeated multiple times
- translations much longer than the source for short inputs
- extreme character elongations not present in the source

It also avoids common false positives like:

- punctuation repetition (`??`)
- natural emphasis (`sooo`)
- source-side repetition that is intentional
- short repeated expressions like `bye bye`

## Running with the provided client

The provided `client.py` expects the server on `http://localhost:8000`.

Suggested workflow:

1. start the API with `uvicorn app.main:app --reload`
2. copy `client.py`, `translation_pairs.jsonl`, `translation_requests.jsonl`, and `stammering_tests.jsonl` into the project root
3. run `python client.py`
4. choose:
   - `1` to populate the database
   - `2` to request prompts
   - `3` to test stammering detection

## Docker

Build:

```bash
docker build -t rag-translation-backend .
```

Run:

```bash
docker run -p 8000:8000 rag-translation-backend
```

## Possible next improvements

- deduplicate identical translation pairs
- persist a precomputed vector index for larger datasets
- add tests with `pytest`
- add logging and structured error handling
- add a `/pairs/bulk` endpoint for faster ingestion
