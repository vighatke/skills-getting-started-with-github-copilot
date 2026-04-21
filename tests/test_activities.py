"""Tests for GET /activities endpoint."""


def test_get_activities_returns_200(client):
    # Arrange
    # No special state needed; default activities are pre-loaded.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200


def test_get_activities_returns_all_nine_activities(client):
    # Arrange
    expected_count = 9

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert len(data) == expected_count


def test_get_activities_each_has_required_fields(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    for name, details in data.items():
        assert required_fields == set(details.keys()), (
            f"Activity '{name}' is missing required fields"
        )


def test_get_activities_participants_is_a_list(client):
    # Arrange
    # Participants must be lists for downstream rendering to work correctly.

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    for name, details in data.items():
        assert isinstance(details["participants"], list), (
            f"Activity '{name}' participants should be a list"
        )


def test_get_activities_chess_club_is_present(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert expected_activity in data
