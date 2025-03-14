from services.user_service.database.database import db
from services.user_service.database.models import FavoriteGame, User


def seed_users() -> None:
    """Seed the Users table with initial test data."""
    seed_users_raw = [
        {"username": "Tom"},
        {"username": "Mark"},
    ]

    for seed_user in seed_users_raw:
        user = User(username=seed_user["username"])

        db.session.add(user)
    db.session.commit()


def seed_favorite_games() -> None:
    """Seed the FavoriteGames table with initial test data."""
    seed_favorite_games_raw = [
        {
            "user_id": 1,
            "game_id": 4,
        },
        {
            "user_id": 1,
            "game_id": 2,
        },
        {
            "user_id": 2,
            "game_id": 2,
        },
    ]

    for seed_favorite_game in seed_favorite_games_raw:
        favorite_game = FavoriteGame(
            user_id=seed_favorite_game["user_id"],
            game_id=seed_favorite_game["game_id"],
        )

        db.session.add(favorite_game)
    db.session.commit()


def seed_database() -> None:
    """Seed the test database with initial data."""
    seed_users()
    seed_favorite_games()
