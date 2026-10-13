import re
import logging
from typing import List, Set, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.schemas.nlp import (
    MatchRequest,
    MatchResponse,
    MatchResult,
    TextSimilarityRequest,
    TextSimilarityResponse,
    SimilarityResult
)

logger = logging.getLogger(__name__)

# Basic fallback English stopwords in case NLTK corpus is uninitialized
DEFAULT_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}

class NLPService:
    def __init__(self):
        self.stopwords = self._load_stopwords()

    def _load_stopwords(self) -> Set[str]:
        try:
            import nltk
            try:
                from nltk.corpus import stopwords
                return set(stopwords.words("english"))
            except LookupError:
                nltk.download("stopwords", quiet=True)
                from nltk.corpus import stopwords
                return set(stopwords.words("english"))
        except Exception as e:
            logger.info("Using fallback stopwords: %s", e)
            return DEFAULT_STOPWORDS

    def tokenize_and_clean(self, text: str) -> List[str]:
        """Tokenize text into lowercase alphanumeric words, filtering stopwords."""
        words = re.findall(r"\b[a-zA-Z0-9_-]+\b", text.lower())
        return [w for w in words if w not in self.stopwords and len(w) > 2]

    def compute_keyword_overlap(self, paper_keywords: List[str], reviewer_keywords: List[str]) -> float:
        """
        Computes Jaccard / overlap coefficient between paper keywords and reviewer expertise.
        """
        if not paper_keywords or not reviewer_keywords:
            return 0.0

        p_set = {k.strip().lower() for k in paper_keywords if k.strip()}
        r_set = {k.strip().lower() for k in reviewer_keywords if k.strip()}

        intersection = p_set.intersection(r_set)
        if not intersection:
            return 0.0

        # Overlap score relative to paper keywords requested
        return round(len(intersection) / len(p_set), 4)

    def match_reviewers(self, request: MatchRequest) -> MatchResponse:
        """
        Core REACH Reviewer Matching Framework:
        1. TF-IDF + Cosine Similarity between paper (title + abstract) and reviewer profiles.
        2. Keyword-based overlap matching.
        3. Workload and Conflict-of-Interest (COI) constraint evaluation.
        """
        paper_text = f"{request.paper_title} {request.paper_abstract}"
        reviewer_texts = [
            f"{' '.join(r.expertise_keywords)} {r.bio_or_abstract or ''}"
            for r in request.reviewers
        ]

        # 1. TF-IDF Cosine Similarity via Scikit-Learn
        tfidf_scores = [0.0] * len(request.reviewers)
        try:
            corpus = [paper_text] + reviewer_texts
            vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
            tfidf_matrix = vectorizer.fit_transform(corpus)
            
            paper_vec = tfidf_matrix[0:1]
            reviewer_vecs = tfidf_matrix[1:]
            
            sims = cosine_similarity(paper_vec, reviewer_vecs)[0]
            tfidf_scores = [round(float(s), 4) for s in sims]
        except Exception as e:
            logger.warning("Error computing TF-IDF similarity: %s", e)

        # 2. Constraints and Ranking
        paper_affiliations = {a.strip().lower() for a in (request.paper_affiliations or []) if a.strip()}
        results: List[MatchResult] = []

        for idx, reviewer in enumerate(request.reviewers):
            tfidf = tfidf_scores[idx]
            kw_score = self.compute_keyword_overlap(request.paper_keywords, reviewer.expertise_keywords)

            # Combined score (60% TF-IDF + 40% Keyword overlap)
            combined = round((0.6 * tfidf) + (0.4 * kw_score), 4)

            # Check Conflict of Interest (e.g. same university/affiliation)
            has_conflict = False
            conflict_reason = None
            reviewer_affiliations = {a.strip().lower() for a in (reviewer.affiliations or []) if a.strip()}
            shared_affils = paper_affiliations.intersection(reviewer_affiliations)
            if shared_affils:
                has_conflict = True
                conflict_reason = f"Shared affiliation: {', '.join(shared_affils)}"

            # Check Workload capacity
            workload_exceeded = (reviewer.current_assignments or 0) >= (reviewer.max_workload or 5)

            results.append(
                MatchResult(
                    reviewer_id=reviewer.id,
                    reviewer_name=reviewer.name,
                    tfidf_score=tfidf,
                    keyword_score=kw_score,
                    combined_score=combined,
                    has_conflict=has_conflict,
                    conflict_reason=conflict_reason,
                    workload_exceeded=workload_exceeded
                )
            )

        # Sort by: valid reviewers first (no conflict & workload ok), then by combined_score descending
        results.sort(
            key=lambda r: (
                not r.has_conflict,
                not r.workload_exceeded,
                r.combined_score
            ),
            reverse=True
        )

        top_k = request.top_k or 5
        return MatchResponse(
            paper_title=request.paper_title,
            total_reviewers_evaluated=len(request.reviewers),
            recommendations=results[:top_k]
        )

    def compute_text_similarity(self, request: TextSimilarityRequest) -> TextSimilarityResponse:
        """Computes pairwise cosine similarity between source text and candidates."""
        corpus = [request.source_text] + request.candidate_texts
        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform(corpus)
        
        source_vec = matrix[0:1]
        candidate_vecs = matrix[1:]
        sims = cosine_similarity(source_vec, candidate_vecs)[0]

        ranked = [
            SimilarityResult(text=candidate, score=round(float(score), 4))
            for candidate, score in zip(request.candidate_texts, sims)
        ]
        ranked.sort(key=lambda x: x.score, reverse=True)

        return TextSimilarityResponse(
            source_text=request.source_text,
            ranked_candidates=ranked
        )

nlp_service = NLPService()
