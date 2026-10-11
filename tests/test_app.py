def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_configured_activities(client):
    # Arrange
    expected_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Team",
        "Art Club",
        "Drama Club",
        "Debate Club",
        "Science Club",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert set(activities) == expected_names
    assert all(
        {"description", "schedule", "max_participants", "participants"}
        <= set(activity)
        for activity in activities.values()
    )


def test_signup_adds_participant(client):
    # Arrange
    activity = "Soccer Team"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity}"
    }
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_duplicate_signup_returns_bad_request(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}
    activities = client.get("/activities").json()
    assert activities[activity]["participants"].count(email) == 1


def test_signup_for_unknown_activity_returns_not_found(client):
    # Arrange
    activity = "Unknown Activity"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity}"
    }
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_from_unknown_activity_returns_not_found(client):
    # Arrange
    activity = "Unknown Activity"
    email = "new.student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregistering_nonparticipant_returns_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "not.signed.up@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up"}
