from flask import current_app
from bson import ObjectId
from ..models.user import User

class UserRepository:

    @staticmethod
    def collection():
        return current_app.mongo.users

    @staticmethod
    def create(user: User):
        result = UserRepository.collection().insert_one(user.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def find_by_id(user_id):
        data = UserRepository.collection().find_one({"_id": ObjectId(user_id)})
        return User.from_mongo(data)

    @staticmethod
    def find_by_email(email):
        data = UserRepository.collection().find_one({"email": email})
        return User.from_mongo(data)

    @staticmethod
    def find_by_username(username):
        data = UserRepository.collection().find_one({"username": username})
        return User.from_mongo(data)

    @staticmethod
    def find_all():
        users = UserRepository.collection().find({})
        return [User.from_mongo(u) for u in users]

    @staticmethod
    def update(user_id, data):
        UserRepository.collection().update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )
        return UserRepository.find_by_id(user_id)

    @staticmethod
    def delete(user_id):
        UserRepository.collection().delete_one({"_id": ObjectId(user_id)})
        return True
