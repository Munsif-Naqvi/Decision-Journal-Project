
def test_signup_success(client):
    data = user_data()

    response1 = client.post("/api/v1/users/signup", json=data)
    assert response1.status_code == 201
    assert response1.get_json()["message"] == "User created successfully"

def test_login_success(client):
    signup_data = user_data()
    login_data = user_data()

    client.post("/api/v1/users/signup", json=signup_data)

    response2 = client.post("/api/v1/users/login", json=login_data)
    body = response2.get_json()

    assert response2.status_code == 200
    assert "access_token" in body

def test_create_decision(client):
    data = user_data()

    client.post("/api/v1/users/signup", json=data)

    login_response = client.post("/api/v1/users/login", json=data)
    login_body = login_response.get_json()
    token = login_body["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    decision_input = decision_data()
    response3 = client.post("/api/v1/decisions/decision", json=decision_input, headers=headers)
    body = response3.get_json()

    assert response3.status_code == 201
    assert body["message"] == "Decision created"

def test_update_decision(client):
    data = user_data()

    client.post("/api/v1/users/signup", json=data)

    login_response = client.post("/api/v1/users/login", json=data)
    login_body = login_response.get_json()
    token = login_body["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    decision_input = decision_data()

    decision_response = client.post("/api/v1/decisions/decision", json=decision_input, headers=headers)
    decision_body = decision_response.get_json()
    decision_id = decision_body["decision_id"]


    update_decision = decision_data()
    response4 = client.put(f"/api/v1/decisions/decision/{decision_id}", json=update_decision, headers=headers)
    body = response4.get_json()

    assert response4.status_code == 200
    assert body["message"] == "Decision updated successfully"


def test_filter_decisions_by_status(client):
    data = user_data()

    client.post("/api/v1/users/signup", json=data)

    login_response = client.post("/api/v1/users/login", json=data)
    login_body = login_response.get_json()
    token = login_body["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    decision_input = decision_data()
    client.post("/api/v1/decisions/decision", json=decision_input, headers=headers)

    response5 = client.get("/api/v1/decisions/?status=OPEN", headers=headers)

    assert response5.status_code == 200

def test_create_review(client):
    data = user_data()

    client.post("/api/v1/users/signup", json=data)

    login_response = client.post("/api/v1/users/login", json=data)
    login_body = login_response.get_json()
    token = login_body["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    decision_input = decision_data()
    decision_response=client.post("/api/v1/decisions/decision", json=decision_input, headers=headers)
    decision_body = decision_response.get_json()
    decision_id = decision_body["decision_id"]

    data_for_review = review_data()
    response6 = client.post(f"/api/v1/reviews/decision/{decision_id}/review", json=data_for_review, headers=headers)
    body = response6.get_json()

    assert response6.status_code == 200
    assert body["message"] == "Review added successfully"


# Meta data
def decision_data():
    return {
        "title": "Making a Flask Project",
        "decision_statement": "Make Flask project instead of Next js",
        "reasoning": "Builds better backend understanding early on",
        "assumptions": "learn backend better",
        "options_considered": "Python Flask, Next js",
        "confidence_level": 85,
        "expected_outcome": "deep backend understanding before moving to Next js."
    }
def user_data():
    return {
        "name": "ali",
        "email": "ali@gmail.com",
        "password": "ali.1234"
    }
def review_data():
    return {
    "actual_outcome": "Worked better than I anticipated",
    "reflection": "I underestimated how valuable relational constraints would be.",
    "lessons_learned": "Choose the database based on long-term maintenance, not short-term convenience.",
    "would_make_same_decision": bool(True)
}