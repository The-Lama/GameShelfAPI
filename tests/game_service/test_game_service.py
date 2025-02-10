import pytest

from services.game_service.exceptions import GameNotFoundError
from services.game_service.game_service import GameService


def test_list_games_with_static_data(setup_database) -> None:
    """Test that all games are listed correctly."""
    games = GameService().list_games()
    assert len(games) == 8
    assert games[0]["name"] == "Die Macher"
    assert games[5]["name"] == "Mare Mediterraneum"


def test_list_games_with_filter(setup_database) -> None:
    """Test that list_games filter works as expected."""
    games = GameService().list_games("chess")
    assert len(games) == 2

    expected_games = {"Buffalo Chess", "Chess"}
    returned_games = {game["name"] for game in games}

    assert expected_games == returned_games


def list_games_with_no_match(setup_database) -> None:
    """Test that list games filter returns None if no match is found."""
    games = GameService().list_games("NonExistentGame")
    assert games == []


@pytest.mark.parametrize(
    "game_id, expected_name",
    [
        (1, "Die Macher"),
        (2, "Dragonmaster"),
        (4, "Tal der Könige"),
    ],
)
def test_get_existing_game_by_id(
    setup_database, game_id: int, expected_name: str
) -> None:
    """Test fetching an existing game by ID."""
    game = GameService().get_game(game_id)
    assert game["name"] == expected_name


def test_get_nonexistent_game_by_id(setup_database) -> None:
    """Test fetching a non-existent game returns None."""
    non_existent_id = 999

    with pytest.raises(GameNotFoundError) as exc_info:
        GameService().get_game(non_existent_id)

    assert str(exc_info.value) == f"Game with ID: {non_existent_id} not found."
