class APIException(Exception):
    status_code = 400
    message = "API error"

    def __init__(self, message=None):
        if message:
            self.message = message

class UsernameTakenError(APIException):
    status_code = 409
    message = "Username already exists"


class EmailTakenError(APIException):
    status_code = 409
    message = "Email already exists"


class SamePasswordError(APIException):
    status_code = 400
    message = "New password must be different"


class InvalidPasswordOrEmail(APIException):
    status_code = 401
    message = "Invalid email or password"

class UserNotFound(APIException):
    status_code = 404
    message = "User not found"