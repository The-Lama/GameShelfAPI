import logging

from flask import Blueprint, g, jsonify, request

logger = logging.getLogger(__name__)

game_routes = Blueprint("game_routes", __name__)


@game_routes.route("/games", methods=["GET"])
def list_games():
    """Return a list of all games."""
    logger.info("Recieved request to list games.")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    name = request.args.get("name", "").lower()

    if page < 1 or limit < 1:
        logger.warning("Invalid pagination parameters provided.")
        return jsonify({"error": "Invalid pagination parameters"}), 400

    games = g.game_service.list_games()
    if name:
        games = [game for game in games if name in game["Name"].lower()]
        logger.debug(f"Filtered games by name containing: {name}")

    start = (page - 1) * limit
    end = start + limit
    paginated_games = games[start:end]

    if not paginated_games:
        logger.warning(f"No games found for page {page} with limit {limit}.")
        return jsonify({"error": "No games found for the given page"}), 404

    logger.info(f"Returning {len(paginated_games)} games for page {page}")
    return jsonify(
        {"page": page, "limit": limit, "total": len(games), "games": paginated_games}
    )


@game_routes.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id):
    """Return details of a game by ID if it exists."""
    logger.info(f"Received requeest to for game with ID: {game_id}")
    game = g.game_service.get_game(game_id)
    if game is None:
        logger.warning(f"Game with ID {game_id} was not found.")
        return jsonify({"error": "Game not found"}), 404
    logger.info(f"Returning game with ID {game_id}")
    return jsonify(game)
