class GameNotFoundError(Exception):
    """Raised when a game is not found."""

    def __init__(self, game_id: int):
        """
        Initialize the exception.

        Args:
            game_id (int): The ID of the game that was not found.
        """
        super().__init__(f"Game with ID: {game_id} not found.")
        self.game_id = game_id


class NoGamesMatchNameFilterError(Exception):
    """Raised when no Game matches the given name_filter."""

    def __init__(self, name_filter: str):
        """
        Initialize the Exception.

        Args:
            name_filter (str): Filter that tries to match the name of the game.
        """
        super().__init__(f"No games found containing: {name_filter}")
        self.name_filter = name_filter
