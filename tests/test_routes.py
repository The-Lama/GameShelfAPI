def test_list_games(client):
    """Test listing pages with pagination."""
    response = client.get("/games?page=1&limit=2")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["games"]) == 2


def test_fiter_games(client):
    """Test filtering games by a name query parameter."""
    response = client.get("/games?name=Chess")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["games"]) == 2
    assert data["games"][1]["Name"] == "Chess"


def test_invalid_pagination(client):
    """Test handling of invalid pagination parameters."""
    response = client.get("/games?page=0&limit=-1")
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_get_game_by_id(client):
    """Test retrieving a game by its ID."""
    response = client.get("/games/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["Name"] == "Die Macher"
