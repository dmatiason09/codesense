"""
good_code.py
Example of clean, well-written Python code.
"""

MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30


class UserManager:
    """Manages user records in memory."""

    def __init__(self):
        """Initialize with an empty user store."""
        self.users = {}

    def add_user(self, user_id: int, name: str, email: str) -> dict:
        """
        Add a new user to the store.

        Args:
            user_id: Unique identifier for the user.
            name: Full name of the user.
            email: Email address of the user.

        Returns:
            The newly created user dictionary.
        """
        if user_id in self.users:
            raise ValueError(f"User {user_id} already exists.")

        user = {"id": user_id, "name": name, "email": email}
        self.users[user_id] = user
        return user

    def get_user(self, user_id: int) -> dict:
        """Return user data by ID, or raise KeyError if not found."""
        if user_id not in self.users:
            raise KeyError(f"No user found with id={user_id}")
        return self.users[user_id]

    def delete_user(self, user_id: int) -> bool:
        """Remove a user from the store. Returns True if removed."""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    def list_users(self) -> list:
        """Return all users as a list."""
        return list(self.users.values())


def format_greeting(name: str, formal: bool = False) -> str:
    """
    Format a greeting message.

    Args:
        name: The person's name.
        formal: If True, use a formal greeting.

    Returns:
        A greeting string.
    """
    if formal:
        return f"Good day, {name}. How may I assist you?"
    return f"Hey {name}! How's it going?"
