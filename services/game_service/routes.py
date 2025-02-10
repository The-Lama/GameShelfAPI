import logging

from flask import Blueprint, Response, jsonify, request

from .exceptions import GameNotFoundError, NoGamesMatchNameFilterError
from .game_service import GameService
from .utils.pagination import (
    InvalidPaginationParametersError,
    PageExceedsDataRangeError,
    paginate,
)

logger = logging.getLogger(__name__)

game_routes = Blueprint("game_routes", __name__)


@game_routes.route("/games", methods=["GET"])
def list_games() -> Response:
    """Return a list of all games."""
    logger.info("Received request to list games.")

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    name_filter = request.args.get("name", "").lower()

    try:
        games = GameService().list_games(name_filter)
        paginated_games = paginate(games, page, limit)

    except NoGamesMatchNameFilterError:
        return jsonify({"games": []}), 200

    except InvalidPaginationParametersError as e:
        return jsonify({"error": str(e)}), 422

    except PageExceedsDataRangeError as e:
        return jsonify({"error": str(e)}), 404

    response = {
        "page": page,
        "limit": limit,
        "total": len(games),
        "games": paginated_games,
    }

    logger.info(f"Returning {len(paginated_games)} games for page {page}")
    return jsonify(response), 200


@game_routes.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id: int) -> Response:
    """Return details of a game by ID if it exists."""
    logger.info(f"Received request to for game with ID: {game_id}")

    try:
        game = GameService().get_game(game_id)
    except GameNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    logger.info(f"Returning game with ID {game_id}")
    return jsonify(game), 200
