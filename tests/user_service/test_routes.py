from flask.testing import FlaskClient


def test_create_user(client: FlaskClient):
    """Test to successfully create a user."""
    payload = {"username": "Alex"}
    response = client.post("/users", json=payload)
    response_data = response.get_json()
    assert response.status_code == 201
    assert response_data["user_id"] == 3
    assert response_data["username"] == "Alex"


def test_get_user(client: FlaskClient):
    """Test to retrieve a user by user_id."""
    response = client.get("/users?user_id=1")
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data["user_id"] == 1
    assert response_data["username"] == "Tom"


def test_get_user_not_found(client: FlaskClient):
    """Test to retrieve a user by a non-existent user_id."""
    response = client.get("/users?user_id=9999")
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data["error"] == "User with user_id '9999' not found"


def test_add_favorite_game(client: FlaskClient):
    """Test to add a favorite game to a user."""
    payload = {"game_id": 3}
    response = client.post("/users/1/favorites", json=payload)
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data["game_id"] == 3


def test_add_favorite_game_user_not_found(client: FlaskClient):
    """Test to add a favorite game to a nonexistent user_id."""
    payload = {"game_id": 3}
    response = client.post("users/9999/favorites", json=payload)
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data["error"] == "User with user_id '9999' not found"


def test_add_favorite_game_twice(client: FlaskClient):
    """Test to add the same favorite game to a user twice."""
    payload = {"game_id": 3}
    response = client.post("users/1/favorites", json=payload)
    response = client.post("users/1/favorites", json=payload)
    response_data = response.get_json()
    assert response.status_code == 409
    assert response_data["error"] == "User_id '1' has already favored game_id '3'"


def test_get_favorite_games(client: FlaskClient):
    """Test to retrieve all favorite games of a user."""
    response = client.get("/users/1/favorites")
    response_data = response.get_json()
    assert response.status_code == 200
    assert len(response_data) == 2
    assert response_data[0]["game_id"] == 4
    assert response_data[1]["game_id"] == 2
