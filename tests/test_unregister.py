"""Tests for DELETE /activities/{activity_name}/signup endpoint."""


def test_unregister_success_returns_200(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # pre-existing participant in seed data

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200


def test_unregister_success_returns_confirmation_message(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    data = response.json()

    # Assert
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    client.delete(f"/activities/{activity}/signup?email={email}")
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]

    # Assert
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404


def test_unregister_participant_not_signed_up_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"  # not in seed data

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404


def test_unregister_then_signup_again_succeeds(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    client.delete(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200


def test_unregister_does_not_affect_other_participants(client):
    # Arrange
    activity = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"

    # Act
    client.delete(f"/activities/{activity}/signup?email={email_to_remove}")
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]

    # Assert
    assert email_to_keep in participants
