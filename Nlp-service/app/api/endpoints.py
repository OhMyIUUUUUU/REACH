from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    HealthResponse,
    TokenizeRequest,
    TokenizeResponse,
    SentimentRequest,
    SentimentResponse,
    SimilarityRequest,
    SimilarityResponse
)
from app.services.nlp_pipeline import nlp_service

router = APIRouter(prefix="/api/nlp", tags=["NLP & Machine Learning"])

@router.get("/health", response_model=HealthResponse)
def get_health():
    return HealthResponse(
        status="ok",
        service="REACH NLP Service",
        version="1.0.0",
        models_loaded=True
    )

@router.post("/tokenize", response_model=TokenizeResponse)
def tokenize_text(payload: TokenizeRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty")
    return nlp_service.get_tokens(payload.text)

@router.post("/sentiment", response_model=SentimentResponse)
def analyze_sentiment(payload: SentimentRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty")
    return nlp_service.analyze_sentiment(payload.text)

@router.post("/similarity", response_model=SimilarityResponse)
def compute_similarity(payload: SimilarityRequest):
    if not payload.source_text.strip():
        raise HTTPException(status_code=400, detail="Source text cannot be empty")
    return nlp_service.compute_similarity(payload.source_text, payload.target_texts)
