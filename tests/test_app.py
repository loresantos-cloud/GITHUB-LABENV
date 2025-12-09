import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_remove_participant():
    # Sign up a new participant
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json().get("message", "")

    # Check participant is in list
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # Remove participant
    remove_resp = client.delete(f"/activities/{activity}/signup?email={email}")
    assert remove_resp.status_code == 200
    assert "Removed" in remove_resp.json().get("message", "")

    # Check participant is removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_signup_duplicate():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Already signed up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "ya está inscrito" in resp.json().get("error", "")
