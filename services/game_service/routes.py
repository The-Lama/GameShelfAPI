import logging

import pandas as pd
from flask import Blueprint, Response, g, jsonify, request

logger = logging.getLogger(__name__)

game_routes = Blueprint("game_routes", __name__)


def paginate(data: pd.DataFrame, page: int, limit: int) -> pd.DataFrame:
    """Return a paginated subset of data based on the given page and limit."""
    logger.debug(f"Pagination parameters - page: {page}, limit: {limit}")
    if page < 1 or limit < 1:
        raise ValueError(
            f"Invalid pagination parameters: page={page}, "
            f"limit={limit}. Both must be >= 1."
        )

    start = (page - 1) * limit
    end = start + limit

    if start >= len(data):
        raise IndexError(f"Page {page} exceeds available data range.")

    return data[start:end]


@game_routes.route("/games", methods=["GET"])
def list_games() -> Response:
    """Return a list of all games."""
    logger.info("Recieved request to list games.")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    name = request.args.get("name", "").lower()

    games = g.game_service.list_games()
    if name:
        games = [game for game in games if name in game["Name"].lower()]
        filtered_count = len(games)
        logger.debug(
            f"Filtered games by name containing: '{name}', "
            f"found {filtered_count} matches."
        )

        if len(games) == 0:
            logger.warning(
                f"No games found with matching the filter criteria: '{name}'"
            )
            return (
                jsonify({"error": "No games found matching the filter criteria"}),
                204,
            )

    try:
        paginated_games = paginate(games, page, limit)
    except ValueError as e:
        logger.warning(e)
        return jsonify({"error": str(e)}), 422
    except IndexError as e:
        logger.warning(e)
        return jsonify({"error": str(e)}), 204

    logger.info(f"Returning {len(paginated_games)} games for page {page}")
    return jsonify(
        {"page": page, "limit": limit, "total": len(games), "games": paginated_games}
    )


@game_routes.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id: int) -> Response:
    """Return details of a game by ID if it exists."""
    logger.info(f"Received request to for game with ID: {game_id}")
    game = g.game_service.get_game(game_id)
    if game is None:
        logger.warning(f"Game with ID {game_id} was not found.")
        return jsonify({"error": "Game not found"}), 404
    logger.info(f"Returning game with ID {game_id}")
    return jsonify(game)
