import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure clean state for the test
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Signing up twice should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_unreg = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_unreg.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should fail
    resp_unreg_again = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_unreg_again.status_code == 400


def test_signup_nonexistent_activity():
    resp = client.post("/activities/NoSuchActivity/signup?email=someone@example.com")
    assert resp.status_code == 404


def test_unregister_nonexistent_activity():
    resp = client.delete("/activities/NoSuchActivity/participants?email=someone@example.com")
    assert resp.status_code == 404
