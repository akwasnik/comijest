class User:
    def __init__(self, username, email, password, _id=None):
        self.id = str(_id) if _id else None
        self.username = username
        self.email = email
        self.password = password  # hashed

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
            username=data["username"],
            email=data["email"],
            password=data["password"],
            _id=data["_id"]
        )
