class User:
    def __init__(self, username, email, password, _id=None):
        self.id = str(_id) if _id else None
        self.username = username
        self.email = email
        self.password = password  # hashed

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def from_mongo_one(data):
        if not data:
            return None
        return User(
            _id=str(data["_id"]),
            username=data["username"],
            email=data["email"],
            password=data["password"],
        )
    
    @staticmethod
    def from_mongo_many(data):
        if not data:
            return None
        return User(
            _id=str(data["_id"]),
            username=data["username"],
            email=data["email"],
        )

