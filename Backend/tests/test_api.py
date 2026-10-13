def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "REACH Backend Service"
    assert "health" in data

def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "uptime" in data

def test_info(client):
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "REACH Backend Service"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"

def test_auth_and_protected_route(client):
    # 1. Register a test user
    user_payload = {
        "email": "testreviewer@reach.edu",
        "username": "reviewer_test",
        "password": "SecurePassword123!",
        "role": "reviewer"
    }
    reg_resp = client.post("/api/auth/register", json=user_payload)
    assert reg_resp.status_code == 201
    reg_data = reg_resp.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == "testreviewer@reach.edu"
    token = reg_data["access_token"]

    # 2. Access /api/auth/me with Bearer token
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = client.get("/api/auth/me", headers=headers)
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["username"] == "reviewer_test"

    # 3. Test Login
    login_payload = {
        "email": "testreviewer@reach.edu",
        "password": "SecurePassword123!"
    }
    login_resp = client.post("/api/auth/login", json=login_payload)
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()

def test_nlp_matching(client):
    match_payload = {
        "paper_title": "Deep Learning for Reviewer Assignment and Natural Language Processing",
        "paper_abstract": "This research explores TF-IDF cosine similarity, keyword matching, and neural representations for conference paper assignment.",
        "paper_keywords": ["nlp", "deep learning", "reviewer matching", "machine learning"],
        "paper_affiliations": ["Quezon City University"],
        "reviewers": [
            {
                "id": "rev-1",
                "name": "Dr. Alan Turing",
                "expertise_keywords": ["nlp", "natural language processing", "information retrieval"],
                "bio_or_abstract": "Specializes in text classification and natural language semantics.",
                "max_workload": 5,
                "current_assignments": 1,
                "affiliations": ["Cambridge University"]
            },
            {
                "id": "rev-2",
                "name": "Prof. Ada Lovelace",
                "expertise_keywords": ["computer architecture", "hardware", "fpga"],
                "bio_or_abstract": "Research in digital electronics and circuit design.",
                "max_workload": 5,
                "current_assignments": 0,
                "affiliations": ["London University"]
            },
            {
                "id": "rev-3",
                "name": "Dr. Conflict Reviewer",
                "expertise_keywords": ["nlp", "deep learning"],
                "bio_or_abstract": "NLP researcher.",
                "max_workload": 5,
                "current_assignments": 0,
                "affiliations": ["Quezon City University"]
            }
        ],
        "top_k": 3
    }
    resp = client.post("/api/nlp/match", json=match_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["recommendations"]) == 3
    top_match = data["recommendations"][0]
    assert top_match["reviewer_name"] == "Dr. Alan Turing"
    assert top_match["has_conflict"] is False
    assert top_match["combined_score"] > 0

    conflict_match = [r for r in data["recommendations"] if r["reviewer_id"] == "rev-3"][0]
    assert conflict_match["has_conflict"] is True
