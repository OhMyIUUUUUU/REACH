import logging
from typing import List, Dict, Any, Optional
from app.models.schemas import (
    TokenizeResponse,
    TokenInfo,
    SentimentResponse,
    SimilarityResponse,
    SimilarityMatch
)

logger = logging.getLogger(__name__)

class NLPPipelineService:
    def __init__(self):
        self._nlp = None
        self._init_spacy()

    def _init_spacy(self):
        try:
            import spacy
            self._nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy en_core_web_sm model successfully.")
        except Exception as e:
            logger.warning("spaCy model load deferred or failed: %s", e)
            self._nlp = None

    def get_tokens(self, text: str) -> TokenizeResponse:
        """
        Tokenizes text using spaCy with linguistic POS tags and lemmatization.
        """
        if self._nlp:
            doc = self._nlp(text)
            tokens = [token.text for token in doc if not token.is_space]
            detailed: List[TokenInfo] = [
                TokenInfo(
                    text=token.text,
                    lemma=token.lemma_,
                    pos=token.pos_,
                    is_stop=token.is_stop
                )
                for token in doc if not token.is_space
            ]
            return TokenizeResponse(
                tokens=tokens,
                token_count=len(tokens),
                detailed_tokens=detailed
            )

        # Fallback basic regex tokenizer
        import re
        words = re.findall(r"\b\w+\b", text)
        detailed = [
            TokenInfo(text=w, lemma=w.lower(), is_stop=w.lower() in {"the", "is", "at", "which", "on", "a", "an", "and", "or"})
            for w in words
        ]
        return TokenizeResponse(tokens=words, token_count=len(words), detailed_tokens=detailed)

    def analyze_sentiment(self, text: str) -> SentimentResponse:
        """
        Lexicon and polarity sentiment analysis.
        """
        pos_words = {"good", "great", "excellent", "amazing", "love", "awesome", "positive", "helpful", "clean", "fast", "best"}
        neg_words = {"bad", "terrible", "poor", "hate", "awful", "negative", "broken", "slow", "error", "fail", "worst"}

        import re
        tokens = re.findall(r"\b\w+\b", text.lower())
        pos_count = sum(1 for t in tokens if t in pos_words)
        neg_count = sum(1 for t in tokens if t in neg_words)
        total = pos_count + neg_count

        if total == 0:
            return SentimentResponse(label="neutral", score=0.5, details={"positive": 0.0, "negative": 0.0})

        pos_ratio = pos_count / total
        neg_ratio = neg_count / total

        if pos_ratio > neg_ratio:
            label = "positive"
            score = round(pos_ratio, 4)
        elif neg_ratio > pos_ratio:
            label = "negative"
            score = round(neg_ratio, 4)
        else:
            label = "neutral"
            score = 0.5

        return SentimentResponse(label=label, score=score, details={"positive": round(pos_ratio, 4), "negative": round(neg_ratio, 4)})

    def compute_similarity(self, source_text: str, target_texts: List[str]) -> SimilarityResponse:
        """
        Computes cosine similarity using Scikit-Learn TfidfVectorizer.
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            corpus = [source_text] + target_texts
            vectorizer = TfidfVectorizer().fit_transform(corpus)
            vectors = vectorizer.toarray()

            source_vec = vectors[0:1]
            target_vecs = vectors[1:]

            similarities = cosine_similarity(source_vec, target_vecs)[0]
            ranked = [
                SimilarityMatch(text=target, score=round(float(score), 4))
                for target, score in zip(target_texts, similarities)
            ]
            ranked.sort(key=lambda m: m.score, reverse=True)
            return SimilarityResponse(source_text=source_text, ranked_matches=ranked)
        except Exception as e:
            logger.warning("Scikit-learn vectorizer fallback: %s", e)
            import math
            import re

            def get_freq(t: str):
                w = re.findall(r"\b\w+\b", t.lower())
                return {x: w.count(x) for x in set(w)}

            s_freq = get_freq(source_text)
            ranked = []
            for tgt in target_texts:
                t_freq = get_freq(tgt)
                dot = sum(s_freq[k] * t_freq.get(k, 0) for k in s_freq)
                norm = math.sqrt(sum(v*v for v in s_freq.values())) * math.sqrt(sum(v*v for v in t_freq.values()))
                score = (dot / norm) if norm > 0 else 0.0
                ranked.append(SimilarityMatch(text=tgt, score=round(score, 4)))
            ranked.sort(key=lambda m: m.score, reverse=True)
            return SimilarityResponse(source_text=source_text, ranked_matches=ranked)

nlp_service = NLPPipelineService()
