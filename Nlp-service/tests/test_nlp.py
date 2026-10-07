from app.services.nlp_pipeline import nlp_service

def test_tokenize():
    text = "Machine learning and natural language processing in REACH."
    res = nlp_service.get_tokens(text)
    assert res.token_count > 0
    assert "learning" in res.tokens

def test_sentiment():
    pos = nlp_service.analyze_sentiment("This system is amazingly fast and helpful!")
    assert pos.label == "positive"

    neg = nlp_service.analyze_sentiment("The server is broken and slow.")
    assert neg.label == "negative"

def test_similarity():
    src = "artificial intelligence machine learning"
    targets = [
        "machine learning algorithms and data",
        "cooking recipes for dinner",
    ]
    res = nlp_service.compute_similarity(src, targets)
    assert len(res.ranked_matches) == 2
    assert res.ranked_matches[0].text == targets[0]
