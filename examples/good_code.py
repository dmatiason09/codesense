"""
simple user manager - stores users in memory
nothing fancy, just a dict wrapper with some validation
"""

MAX_USERNAME_LEN = 32
MIN_PASSWORD_LEN = 8


class UserManager:
    """handles user storage and basic operations"""

    def __init__(self):
        self.users = {}
        self._next_id = 1

    def add_user(self, username, email, password):
        """
        add a new user. raises ValueError if username taken or inputs invalid.
        returns the new user dict on success.
        """
        if not username or len(username) > MAX_USERNAME_LEN:
            raise ValueError(f"username must be between 1 and {MAX_USERNAME_LEN} chars")

        if username in self.users:
            raise ValueError(f"username '{username}' is already taken")

        if len(password) < MIN_PASSWORD_LEN:
            raise ValueError(f"password too short (min {MIN_PASSWORD_LEN} chars)")

        user = {
            "id": self._next_id,
            "username": username,
            "email": email,
            # not storing plain passwords in real life obviously
            "password_hash": hash(password)
        }
        self.users[username] = user
        self._next_id += 1
        return user

    def get_user(self, username):
        if username not in self.users:
            raise KeyError(f"user '{username}' not found")
        return self.users[username]

    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            return True
        return False

    def all_users(self):
        return list(self.users.values())

    def count(self):
        return len(self.users)


def format_welcome(username, is_admin=False):
    """returns a welcome message, admins get a different one"""
    if is_admin:
        return f"Welcome back, {username}. Admin panel is accessible from the dashboard."
    return f"Hey {username}, good to see you!"
