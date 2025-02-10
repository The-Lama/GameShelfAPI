import logging

from flask import Blueprint, Response, jsonify

from .exceptions import (
    DatabaseError,
    GameAlreadyInFavoritesError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from .user_service import UserService
from .utils.parameter_validation import (
    validate_json_parameters,
    validate_query_parameters,
)

logger = logging.getLogger(__name__)

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/users", methods=["POST"])
@validate_json_parameters(("username", str))
def create_user(username) -> Response:
    """
    Create a new user.

    Args:
        username (str): The username of the new user.

    Returns:
        Response: JSON response with user data if successful.
        Returns 409 if the user already exists.
        Returns 500 if a database error occurs.
    """
    logger.info("Received request to create a new user.")

    try:
        user = UserService().create_user(username)

    except UserAlreadyExistsError as e:
        return jsonify({"error": str(e)}), 409

    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500

    logger.info(f"created user: {username}")
    return jsonify(user), 201


@user_routes.route("/users", methods=["GET"])
@validate_query_parameters(("user_id", int))
def get_user(user_id: int) -> Response:
    """
    Get user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        Response: JSON response containing user data.
        Returns 400 is the user is not found.
    """
    logger.info("Received request to get user by id.")

    try:
        user = UserService().get_user(user_id)

    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(user), 200


@user_routes.route("/users/favorites", methods=["POST"])
@validate_json_parameters(("user_id", int), ("game_id", int))
def add_favorite_game(user_id: int, game_id: int) -> Response:
    """
    Add a game to a user's favorite games.

    Args:
        user_id (int): The ID of the user.
        game_id (int): The ID of the game to be added to favorites.

    Returns:
        Response: JSON response with the id pair user_id and game_id.
        Returns 409 if the game is already in the user's favorites.
        Returns 400 if the user is not found.
        Returns 500 for a database error.
    """
    logger.debug("Received request to add a user's favorite game.")
    logger.info(
        f"Adding game with game_id: {game_id} to user {user_id}'s favorite games."
    )

    try:
        favorite_game = UserService().add_favorite_game(user_id, game_id)

    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 400

    except GameAlreadyInFavoritesError as e:
        return jsonify({"error": str(e)}), 409

    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(favorite_game), 200


@user_routes.route("/users/favorites", methods=["GET"])
@validate_query_parameters(("user_id", int))
def get_favorite_games(user_id: int) -> Response:
    """
    Retrieve a user's favorite games.

    Args:
        user_id (int): The ID of a user.

    Returns:
        Response: JSON response containing the list of favorite games.
        Returns 400 if the user is not found.
    """
    logger.debug("Received request to list favorite games of user.")

    try:
        favorite_games = UserService().get_favorite_games(user_id)

    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(favorite_games), 200
