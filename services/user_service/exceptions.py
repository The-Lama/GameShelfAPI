class UserAlreadyExistsError(Exception):
    """Raised when attempting to create a user that already exists."""

    def __init__(self, username: str):
        """
        Initialize the exception.

        Args:
            username (str): The username that is already taken.
        """
        super().__init__(f"Username '{username}' is already taken")
        self.username = username


class UserNotFoundError(Exception):
    """Raised when a user is not found."""

    def __init__(self, user_id):
        """
        Initialize the exception.

        Args:
            user_id (str): The ID of the user that was not found.
        """
        super().__init__(f"User with user_id '{user_id}' not found")
        self.user_id = user_id


class GameAlreadyInFavoritesError(Exception):
    """
    Raised when a user tries to add a game to their favorites list.

    This error occurs if the game is already in the user's favorites.
    """

    def __init__(self, user_id, game_id):
        """
        Initialize the exception.

        Args:
            user_id (int): The ID of the user.
            game_id (int): The ID of the game that is already in favorites.
        """
        super().__init__(f"User_id '{user_id}' has already favored game_id '{game_id}'")
        self.user_id = user_id
        self.game_id = game_id


class DatabaseError(Exception):
    """Raised for general database errors."""

    def __init__(self, message: str):
        """
        Initialize the exception.

        Args:
            message (str): A descriptive message explaining the database error.
        """
        super().__init__(self, message)
