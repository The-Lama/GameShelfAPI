import pytest
from services.game_service.game_service import GameService


@pytest.fixture
def test_game_service():
    test_data_path = "tests/test_data/games_test.csv"
    return GameService(dataset_path=test_data_path)


def test_list_games(test_game_service):
    games = test_game_service.list_games()
    assert len(games) == 5
    assert games[0]["Name"] == "Die Macher"


def test_get_game_found(test_game_service):
    game = test_game_service.get_game(2)
    assert game["Name"] == "Dragonmaster"


def test_get_game_not_found(test_game_service):
    game = test_game_service.get_game(99)
    assert game is None
