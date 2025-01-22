import pytest

from services.game_service.app import app
from services.game_service.game_service import GameService


@pytest.fixture
def static_game_service():
    """Create a GameService fixture using predefined static data."""
    static_games = [
        {"BGGId": 1, "Name": "Die Macher"},
        {"BGGId": 2, "Name": "Dragonmaster"},
        {"BGGId": 3, "Name": "Samurai"},
        {"BGGId": 4, "Name": "Tal der Könige"},
        {"BGGId": 5, "Name": "Acquire"},
        {"BGGId": 6, "Name": "Mare Mediterraneum"},
    ]
    service = GameService.from_static_data(static_games)
    return service


@pytest.fixture(scope="module")
def csv_game_service():
    """Create a GameService fixture using data from a CSV file."""
    return GameService("tests/data/games_test.csv")


@pytest.fixture
def client(static_game_service):
    """Create a Flask test client using the static game service."""
    app.config["TESTING"] = True
    app.config["GAME_SERVICE"] = static_game_service
    with app.test_client() as client:
        yield client
