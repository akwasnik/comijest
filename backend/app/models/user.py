from app import mongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError

class User:
    collection = mongo.db.users

    def __init__(self, username, email, password,_id=None):
        self.id = _id
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.username,
            "password": self.password
        }
    
    @staticmethod
    def from_mongo(data):
        if not data:
            return None
        return User(
            username=data['username'],
            email=data['email'],
            _id=str(data["_id"])
        )
    
    def save(self):
        try:
            result = self.collection.insert_one(self.to_dict())
            self.id = str(result.inserted_id)
            return self.id
        except DuplicateKeyError:
            return {"error": "User already exists"}
        
    @classmethod
    def find_by_id(cls, user_id):
        data = cls.collection.find_one({"_id": ObjectId(user_id)})
        return cls.from_mongo(data)
    
    @classmethod
    def find_by_username(cls, username):
        data = cls.collection.find_one({"username": username})
        return cls.from_mongo(data)
    
    @classmethod
    def find_by_username(cls, email):
        data = cls.collection.find_one({"email": email})
        return cls.from_mongo(data)