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


@game_routes.errorhandler(NoGamesMatchNameFilterError)
def handle_no_games_match_name_filter(error: NoGamesMatchNameFilterError) -> Response:
    """
    Handle the case where no game matches the name filter.

    Args:
        error (NoGamesMatchNameFilterError): Exception instance.

    returns: A JSON response with an empty list.
    """
    logger.error(f"No games match the filter: {error.name_filter}")
    return jsonify({"games": []}), 200


@game_routes.errorhandler(GameNotFoundError)
def handle_game_not_found(error: GameNotFoundError) -> Response:
    """
    Handle the case where a game was not found.

    Args:
        error: (GameNotFoundError): Exception instance.

    Returns: 404 status code.
    """
    logger.error(f"Game not found: {error.game_id}")
    return jsonify({"error": str(error)}), 404


@game_routes.errorhandler(InvalidPaginationParametersError)
def handle_invalid_pagination_parameters(
    error: InvalidPaginationParametersError,
) -> Response:
    """
    Handle the case when the pagination parameters are invalid.

    Args:
        error (InvalidPaginationParametersError): Exception instance.

    Returns: 422 status code.
    """
    logger.error(
        f"Invalid pagination parameters: page: {error.page}, limit: {error.limit}"
    )
    return jsonify({"error": str(error)}), 422


@game_routes.errorhandler(PageExceedsDataRangeError)
def handle_page_exceeds_data_range(error: PageExceedsDataRangeError) -> Response:
    """
    Handle the case when the requested page exceeds the available data range.

    Args:
        error (PageExceedsDataRangeError): Exception instance.

    Returns: 404 status code
    """
    logger.error(f"Page {error.page} exceeds data range.")
    return jsonify({"error": str(error)}), 404


@game_routes.route("/games", methods=["GET"])
def list_games() -> Response:
    """
    Retrieve and return a paginated list of games.

    Query Parameters:
        page (int, optional): The page number to retrieve (Default is 1).
        limit (int, optional): The number of games per page (Default is 10).
        name (str, optional): A name filter to apply to the list of games.

    Returns:
        Response: A JSON response with the following structure:
            {
                "page": <current_page>,
                "limit": <limit_per_page>,
                "total": <total_number_of_games>,
                "games": <list_of_games_for_current_page>
            }
    """
    logger.info("Received request to list games.")

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    name_filter = request.args.get("name", "").lower()

    games = GameService().list_games(name_filter)
    paginated_games = paginate(games, page, limit)

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
    """
    Retrieve details of a specific game by ID.

    Args:
        game_id (int): The unique identifier of the game to be retrieved.

    returns:
        Response: A JSON response containing details of the game.
    """
    logger.info(f"Received request to for game with ID: {game_id}")

    game = GameService().get_game(game_id)

    logger.info(f"Returning game with ID {game_id}")
    return jsonify(game), 200
