from flask.testing import FlaskClient


def test_list_games(client: FlaskClient) -> None:
    """Test listing pages with pagination."""
    response = client.get("/games?page=1&limit=2")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["games"]) == 2


def test_filter_games(client: FlaskClient) -> None:
    """Test filtering games by a name query parameter."""
    response = client.get("/games?name=Chess")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["games"]) == 2

    expected_games = {"Buffalo Chess", "Chess"}
    returned_games = {game["name"] for game in data["games"]}

    assert expected_games == returned_games


def test_invalid_pagination(client: FlaskClient) -> None:
    """Test handling of invalid pagination parameters."""
    response = client.get("/games?page=0&limit=-1")
    data = response.get_json()

    assert response.status_code == 422
    assert "error" in data


def test_pagination_out_of_bounds(client: FlaskClient) -> None:
    """Test pagination when requesting a page beyond available data."""
    response = client.get("/games?page=1000&limit=10")
    data = response.get_json()

    assert response.status_code == 404
    assert "error" in data


def test_get_game_by_id(client: FlaskClient) -> None:
    """Test retrieving a game by its ID."""
    response = client.get("/games/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "Die Macher"
