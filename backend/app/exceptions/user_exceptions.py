class UsernameTakenError(Exception):
    """Raised when trying to use a username that already exists."""
    pass

class EmailTakenError(Exception):
    """Raised when trying to use an email that already exists."""
    pass

class SamePasswordError(Exception):
    """Raised when new password is identical to current password."""
    pass
class InvalidPasswordOrEmail(Exception):
    """Raised when invalid password or email are provided for login"""
    pass