import logging

from .database import db

logger = logging.getLogger(__name__)


class User(db.Model):
    """
    Represents a user entity in the database.

    Attributes:
        user_id (int): The unique identifier for the user.
        username (str): The unique username chosen by the user.
    """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def to_dict(self) -> dict:
        """Convert the User object into a dictonary."""
        return {"user_id": self.user_id, "username": self.username}


class FavoriteGame(db.Model):
    """
    Represents a board game that the user likes.

    Attributes:
        favorite_id (int): The unique identifier for the favorite game entry.
        user_id (int): The ID of the user who favorited the game.
        game_id (int): The ID of the board game marked as favorite.
    """

    __tablename__ = "favorite_games"

    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    game_id = db.Column(db.Integer, nullable=False)

    def to_dict(self) -> dict:
        """Convert the FavoriteGame object into a dictornary."""
        return {"user_id": self.user_id, "game_id": self.game_id}
