class User:
    def __init__(self, username, email, password=None, role="user",_id=None):
        self.id = str(_id) if _id else None
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "password": self.password
        }

    def to_public_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }

    def to_auth_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "password": self.password
        }
    @staticmethod
    def from_mongo(data):
        if not data:
            return None
        return User(
            _id=data["_id"],
            username=data["username"],
            email=data["email"],
            password=data.get("password"),
            role=data.get("role", "user")
        )
