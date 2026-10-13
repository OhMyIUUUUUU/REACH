from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Health Schema
class NLPHealthResponse(BaseModel):
    status: str = "ok"
    service: str = "REACH NLP & Reviewer Matching Service"
    version: str = "1.0.0"
    models_loaded: bool = True

# Tokenization Schemas
class TokenizeRequest(BaseModel):
    text: str = Field(..., description="Raw text string to tokenize and clean")

class TokenInfo(BaseModel):
    text: str
    lemma: Optional[str] = None
    pos: Optional[str] = None
    is_stop: Optional[bool] = None

class TokenizeResponse(BaseModel):
    tokens: List[str]
    token_count: int
    detailed_tokens: Optional[List[TokenInfo]] = None

# Sentiment Schemas
class SentimentRequest(BaseModel):
    text: str = Field(..., description="Text input for sentiment classification")

class SentimentResponse(BaseModel):
    label: str  # positive, negative, neutral
    score: float
    details: Optional[Dict[str, float]] = None

# Reviewer Matching Schemas
class ReviewerProfile(BaseModel):
    id: str
    name: str
    expertise_keywords: List[str]
    bio_or_abstract: Optional[str] = ""
    max_workload: Optional[int] = 5
    current_assignments: Optional[int] = 0
    affiliations: Optional[List[str]] = Field(default_factory=list)

class MatchRequest(BaseModel):
    paper_id: Optional[str] = None
    paper_title: str
    paper_abstract: str
    paper_keywords: List[str] = Field(default_factory=list)
    paper_authors: Optional[List[str]] = Field(default_factory=list)
    paper_affiliations: Optional[List[str]] = Field(default_factory=list)
    reviewers: List[ReviewerProfile]
    top_k: Optional[int] = 5

class MatchResult(BaseModel):
    reviewer_id: str
    reviewer_name: str
    tfidf_score: float
    keyword_score: float
    combined_score: float
    has_conflict: bool = False
    conflict_reason: Optional[str] = None
    workload_exceeded: bool = False

class MatchResponse(BaseModel):
    paper_title: str
    total_reviewers_evaluated: int
    recommendations: List[MatchResult]

# Text Similarity Schemas
class TextSimilarityRequest(BaseModel):
    source_text: str
    candidate_texts: List[str]

class SimilarityResult(BaseModel):
    text: str
    score: float

class TextSimilarityResponse(BaseModel):
    source_text: str
    ranked_candidates: List[SimilarityResult]
