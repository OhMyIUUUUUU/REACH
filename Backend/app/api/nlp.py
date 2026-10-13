from typing import List
from fastapi import APIRouter
from app.schemas.nlp import (
    MatchRequest,
    MatchResponse,
    TextSimilarityRequest,
    TextSimilarityResponse
)
from app.services.nlp_service import nlp_service

router = APIRouter(prefix="/nlp", tags=["NLP & Reviewer Matching"])

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

@router.post(
    "/similarity",
    response_model=TextSimilarityResponse,
    summary="Compute TF-IDF text similarity"
)
def compute_similarity(request: TextSimilarityRequest) -> TextSimilarityResponse:
    """Computes cosine similarity ranking between a source text and multiple candidate texts."""
    return nlp_service.compute_text_similarity(request)

@router.post(
    "/tokenize",
    summary="Tokenize text with stopword filtering"
)
def tokenize_text(text: str) -> List[str]:
    """Tokenizes text using NLTK/regex stopword filtering."""
    return nlp_service.tokenize_and_clean(text)
