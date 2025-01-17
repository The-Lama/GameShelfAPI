from flask import Blueprint, jsonify

from services.game_service.game_service import GameService

game_routes = Blueprint("game_routes", __name__)
game_service = GameService()


@game_routes.route("/games", methods=["GET"])
def list_games():
    """Return a list of all games."""
    return jsonify(game_service.list_games())


@game_routes.route("/games/<int:id>", methods=["GET"])
def get_game(game_id):
    """Return details of a game by ID if it exists."""
    game = game_service.get_game(game_id)
    if game is None:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(game)
