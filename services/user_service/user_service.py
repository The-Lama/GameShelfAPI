import logging
from typing import List, TypedDict

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .database.database import db
from .database.models import FavoriteGame, User
from .exceptions import (
    DatabaseError,
    GameAlreadyInFavoritesError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

logger = logging.getLogger(__name__)


class UserDict(TypedDict):
    """A TypedDict representing a user."""

    user_id: int
    username: str


class FavoriteGameDict(TypedDict):
    """A TypedDict representing a user's favorite game."""

    user_id: int
    game_id: int


class UserService:
    """A service for managing user data."""

    def _ensure_user(self, user_id: int) -> User:
        """
        Retrieve a user or raise an error if not found.

        Args:
            user_id (int): The unique ID of the user.

        Returns:
            User: The User Object containing user details.

        Raises:
            UserNotFoundError: If the user does not exist.
        """
        user = User.query.filter_by(user_id=user_id).one_or_none()
        if not user:
            logger.warning(f"User with user_id {user_id} not found.")
            raise UserNotFoundError(user_id)
        return user

    def create_user(self, username: str) -> UserDict:
        """
        Create a new user with the given username.

        Args:
            username (str): The desired username.

        Returns:
            UserDict: A dictionary containing the user's details.

        Raises:
            UserAlreadyExistsError: If the username is already taken.
            DatabaseError: If a database error occurs.
        """
        user = User(username=username)
        try:
            db.session.add(user)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Username {username} is already taken.")
            raise UserAlreadyExistsError(username) from e

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error creating username: '{username}': {e}")
            raise DatabaseError(f"Failed to create user '{username}'") from e

        logger.info(f"User '{username}' created successfully.")
        return user.to_dict()

    def get_user(self, user_id: int) -> UserDict:
        """
        Retrieve a user by id.

        Args:
            user_id (int): The unique ID of the user.

        Returns:
            UserDict: A dictionary containing the user's details.

        Raises:
            UserNotFoundError: If the user does not exist.
        """
        logger.debug(f"Fetching user with user_id: '{user_id}'")

        user = self._ensure_user(user_id)

        logger.debug(f"Found user '{user.username}' with user_id: {user.user_id}")
        return user.to_dict()

    def add_favorite_game(self, user_id: int, game_id: int) -> FavoriteGameDict:
        """
        Add a game to a user's favorite games.

        Args:
            user_id (int): The unique ID of the user.
            game_id (int): The unique ID of the game.

        Returns:
            FavoriteGameDict: A dictionary containing the IDs of user_id and game_id

        Raises:
            UserNotFoundError: If the user does not exist.
            GameAlreadyFavored: If the game is already favored by the user.
            DatabaseError: If a database error occurs.
        """
        self._ensure_user(user_id)

        if FavoriteGame.query.filter_by(user_id=user_id, game_id=game_id).first():
            logging.warning(f"User {user_id} has already favored game {game_id}")
            raise GameAlreadyInFavoritesError(user_id, game_id)

        favorite_game = FavoriteGame(user_id=user_id, game_id=game_id)
        try:
            db.session.add(favorite_game)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error adding favorite game {game_id} to user {user_id}: {e}")
            raise DatabaseError(
                f"Failed to add favorite game {game_id} to user {user_id}"
            ) from e

        logger.info(f"Favorite Game with game_id {game_id} was added to user {user_id}")
        return favorite_game.to_dict()

    def get_favorite_games(self, user_id: int) -> List[FavoriteGameDict]:
        """
        Retrieve a user's favorite games.

        Args:
            user_id (int): The unique ID of the user.

        Returns:
            List[FavoriteGames]: A list of dictionaries containing
                the ID of the user and the game.

        Raises:
            UserNotFoundError: If the user does not exist.
        """
        self._ensure_user(user_id)

        favorite_games = FavoriteGame.query.filter_by(user_id=user_id).all()

        logger.debug(f"Found {len(favorite_games)} favorite games of user {user_id}")
        return [game.to_dict() for game in favorite_games]
