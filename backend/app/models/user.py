from werkzeug.security import generate_password_hash, check_password_hash


class User:

    def __init__(self, username, email, password, _id=None, hashed=False):
        self.id = str(_id) if _id else None
        self.username = username
        self.email = email
        self.password = password if hashed else generate_password_hash(password)

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def from_mongo(data):
        if not data:
            return None

        return User(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            _id=data.get("_id"),
            hashed=True
        )

    def verify_password(self, password):
        return check_password_hash(self.password, password)
