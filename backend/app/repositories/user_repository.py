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
        cursor = UserRepository.collection().find(
            {},
            {"username": 1, "email": 1}
        )
        return [User.from_mongo(u) for u in cursor]

    @staticmethod
    def update(user_id, data):
        updated = UserRepository.collection().update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )
        return updated.acknowledged

    @staticmethod
    def delete(user_id):
        UserRepository.collection().delete_one({"_id": ObjectId(user_id)})
        return True

    @staticmethod
    def find_by_email_for_login(email):
        data = UserRepository.collection().find_one(
            {"email": email},
            {"username": 1, "email": 1, "password": 1, "role": 1}
        )
        return User.from_mongo(data)
