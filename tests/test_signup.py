"""Tests for POST /activities/{activity_name}/signup endpoint."""


def test_signup_success_returns_200(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200


def test_signup_success_returns_confirmation_message(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    data = response.json()

    # Assert
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    client.post(f"/activities/{activity}/signup?email={email}")
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]

    # Assert
    assert email in participants


def test_signup_duplicate_email_returns_409(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already a participant in seed data

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 409


def test_signup_duplicate_email_returns_detail_message(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    data = response.json()

    # Assert
    assert "detail" in data
    assert email in data["detail"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404


def test_signup_unknown_activity_returns_detail_message(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    data = response.json()

    # Assert
    assert "detail" in data
