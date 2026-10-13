from typing import Optional, Union, List
from fastapi import APIRouter, HTTPException, Query, Body
from app.schemas.nlp import (
    NLPHealthResponse,
    MatchRequest,
    MatchResponse,
    TextSimilarityRequest,
    TextSimilarityResponse,
    TokenizeRequest,
    TokenizeResponse,
    SentimentRequest,
    SentimentResponse
)
from app.services.nlp_service import nlp_service

router = APIRouter(prefix="/nlp", tags=["NLP & Reviewer Matching"])

@router.get(
    "/health",
    response_model=NLPHealthResponse,
    summary="NLP engine health check"
)
def get_nlp_health() -> NLPHealthResponse:
    """Returns NLP subservice health and model loading status."""
    return NLPHealthResponse(
        status="ok",
        service="REACH NLP & Reviewer Matching Engine",
        version="1.0.0",
        models_loaded=True
    )

@router.post(
    "/tokenize",
    response_model=Union[TokenizeResponse, List[str]],
    summary="Tokenize text with linguistic filtering"
)
def tokenize_text(
    payload: Optional[TokenizeRequest] = Body(None),
    text: Optional[str] = Query(None)
):
    """
    Tokenizes text input. Accepts either a JSON body:
      {"text": "example sentence"}
    or a query parameter:
      ?text=example+sentence
    """
    raw_text = payload.text if payload and payload.text else text
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=400, detail="Text parameter or JSON body is required.")

    if payload:
        return nlp_service.get_detailed_tokens(raw_text)
    return nlp_service.tokenize_and_clean(raw_text)

@router.post(
    "/sentiment",
    response_model=SentimentResponse,
    summary="Analyze sentiment polarity"
)
def analyze_sentiment(payload: SentimentRequest) -> SentimentResponse:
    """Analyzes text sentiment and returns polarity label (positive, neutral, negative) and score."""
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    return nlp_service.analyze_sentiment(payload.text)

@router.post(
    "/similarity",
    response_model=TextSimilarityResponse,
    summary="Compute TF-IDF text similarity"
)
def compute_similarity(request: TextSimilarityRequest) -> TextSimilarityResponse:
    """Computes TF-IDF cosine similarity between source text and candidates."""
    if not request.source_text.strip():
        raise HTTPException(status_code=400, detail="Source text cannot be empty.")
    return nlp_service.compute_text_similarity(request)

@router.post(
    "/match",
    response_model=MatchResponse,
    summary="Match reviewers to paper using NLP & constraints"
)
def match_reviewers(request: MatchRequest) -> MatchResponse:
    """
    Executes the REACH Reviewer Matching Framework:
    - Scikit-Learn TF-IDF vectorization and cosine similarity
    - Keyword overlap coefficient
    - Conflict of interest (COI) filtering
    - Workload limit verification
    """
    return nlp_service.match_reviewers(request)
