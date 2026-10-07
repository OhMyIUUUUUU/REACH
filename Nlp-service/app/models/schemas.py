from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "REACH NLP & Machine Learning Service"
    version: str = "1.0.0"
    models_loaded: bool = False

class TokenizeRequest(BaseModel):
    text: str = Field(..., description="Raw text string to tokenize and analyze")

class TokenInfo(BaseModel):
    text: str
    lemma: Optional[str] = None
    pos: Optional[str] = None
    is_stop: Optional[bool] = None

class TokenizeResponse(BaseModel):
    tokens: List[str]
    token_count: int
    detailed_tokens: Optional[List[TokenInfo]] = None

class SentimentRequest(BaseModel):
    text: str = Field(..., description="Text input for sentiment classification")

class SentimentResponse(BaseModel):
    label: str  # positive, negative, neutral
    score: float
    details: Optional[Dict[str, float]] = None

class EmbeddingRequest(BaseModel):
    texts: List[str] = Field(..., description="List of text chunks to compute vector embeddings for")

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    dimension: int
    count: int

class SimilarityRequest(BaseModel):
    source_text: str
    target_texts: List[str]

class SimilarityMatch(BaseModel):
    text: str
    score: float

class SimilarityResponse(BaseModel):
    source_text: str
    ranked_matches: List[SimilarityMatch]
