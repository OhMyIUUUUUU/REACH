# REACH NLP & Machine Learning Service

Natural Language Processing and Machine Learning inference microservice for the REACH platform.

## Architecture & Directory Layout

```
Nlp-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & CORS configuration
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py     # Endpoints: /tokenize, /sentiment, /similarity, /health
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Settings & environment configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic data request/response schemas
│   └── services/
│       ├── __init__.py
│       └── nlp_pipeline.py  # NLP pipeline & ML algorithms
├── data/                    # Corpora, training datasets, and vocabulary
├── saved_models/            # Local model weights, fine-tuned checkpoints, vector indexes
├── tests/
│   └── test_nlp.py          # Unit tests
├── requirements.txt         # NLP, ML, and API package dependencies
├── .gitignore               # Ignores large models, datasets, venv, and cache
└── README.md
```

## Packages Included

| Package | Category | Purpose |
| :--- | :--- | :--- |
| **`fastapi`** & **`uvicorn`** | API / Serving | High-throughput asynchronous REST API for Go backend and React |
| **`spacy`** | Industrial NLP | Tokenization, POS tagging, Lemmatization, Named Entity Recognition (NER) |
| **`nltk`** | Classic NLP | Tokenizers, corpus access, stopwords, stemming |
| **`transformers`** | Deep Learning | Hugging Face transformer models (BERT, RoBERTa, LLMs) |
| **`sentence-transformers`** | Embeddings | High-speed dense text embeddings & semantic search |
| **`scikit-learn`** | Machine Learning | TF-IDF, classification, clustering, evaluation metrics |
| **`torch`** | Neural Networks | PyTorch framework for deep learning inference |
| **`numpy`** & **`pandas`** | Data / Math | Tensor math, vector transformations, and data analysis |
| **`pydantic`** | Validation | Strict data validation and OpenAPI schema generation |

## Setup & Quickstart

### 1. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Packages
```bash
pip install -r requirements.txt
```

*(Optional) Download spaCy English language model:*
```bash
python -m spacy download en_core_web_sm
```

### 3. Start the NLP Service
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

Interactive API documentation (Swagger UI) will be live at:
```
http://localhost:5000/docs
```

## API Endpoints

- `GET /` - Service status and documentation links
- `GET /api/nlp/health` - Health check & model status
- `POST /api/nlp/tokenize` - Tokenize text and extract linguistic features
- `POST /api/nlp/sentiment` - Sentiment classification
- `POST /api/nlp/similarity` - Text ranking and cosine similarity
