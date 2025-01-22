import pytest


def test_list_games_with_static_data(static_game_service):
    """Test that all games are listed correctly."""
    games = static_game_service.list_games()
    assert len(games) == 6
    assert games[0]["Name"] == "Die Macher"
    assert games[5]["Name"] == "Mare Mediterraneum"


@pytest.mark.parametrize(
    "game_id, expected_name",
    [
        (1, "Die Macher"),
        (2, "Dragonmaster"),
        (4, "Tal der Könige"),
    ],
)
def test_get_existing_game_by_id_static(static_game_service, game_id, expected_name):
    """Test fetching an existing game by ID."""
    game = static_game_service.get_game(game_id)
    assert game["Name"] == expected_name


def test_get_nonexisten_by_id_static(static_game_service):
    """Test fetching a non-existent game returns None."""
    game = static_game_service.get_game(999)
    assert game is None


def test_csv_game_service_integration(csv_game_service):
    """ "Integration Test: Ensure the CSV service works end-to-end."""
    games = csv_game_service.list_games()
    assert len(games) == 5
    assert games[0]["Name"] == "Die Macher"
    assert games[0]["BGGId"] == 1

    game = csv_game_service.get_game(2)
    assert game["Name"] == "Dragonmaster"
