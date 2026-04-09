"""
Tests for the Mergington High School Activities API

Uses the AAA (Arrange-Act-Assert) testing pattern for clarity and consistency.
"""

from fastapi.testclient import TestClient
from src.app import app


def test_get_activities():
    """Test that GET /activities returns all available activities"""
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    # Verify structure of an activity
    first_activity = list(activities.values())[0]
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    assert isinstance(first_activity["participants"], list)


def test_signup_for_activity():
    """Test that POST /activities/{activity_name}/signup adds a student"""
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]
    # Verify student was added to participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_unregister_from_activity():
    """Test that DELETE /activities/{activity_name}/unregister removes a student"""
    # Arrange
    client = TestClient(app)
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already registered

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]
    # Verify student was removed from participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]
