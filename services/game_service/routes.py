import logging

from flask import Blueprint, Response, jsonify, request

from .game_service import GameService
from .utils.pagination import paginate

logger = logging.getLogger(__name__)

game_routes = Blueprint("game_routes", __name__)


@game_routes.route("/games", methods=["GET"])
def list_games() -> Response:
    """Return a list of all games."""
    logger.info("Recieved request to list games.")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    name_filter = request.args.get("name", "").lower()

    games = GameService().list_games(name_filter)
    if name_filter and not games:
        logger.warning(
            f"No games found with matching the filter criteria: '{name_filter}'"
        )
        return (
            jsonify({"error": "No games found matching the filter criteria"}),
            204,
        )

    try:
        paginated_games = paginate(games, page, limit)
    except (ValueError, IndexError) as e:
        logger.warning(f"Pagination error: {e}")
        status_code = 422 if isinstance(e, ValueError) else 404
        return jsonify({"error": str(e)}), status_code

    response = {
        "page": page,
        "limit": limit,
        "total": len(games),
        "games": paginated_games,
    }

    logger.info(f"Returning {len(paginated_games)} games for page {page}")
    return jsonify(response)


@game_routes.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id: int) -> Response:
    """Return details of a game by ID if it exists."""
    logger.info(f"Received request to for game with ID: {game_id}")

    game = GameService().get_game(game_id)

    if game is None:
        logger.warning(f"Game with ID {game_id} was not found.")
        return jsonify({"error": "Game not found"}), 404

    logger.info(f"Returning game with ID {game_id}")
    return jsonify(game)
