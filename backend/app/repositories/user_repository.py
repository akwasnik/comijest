from bson.objectid import ObjectId
from ..extensions import mongo


class UserRepository:

    @staticmethod
    def insert(user_dict):
        return mongo.db.users.insert_one(user_dict)

    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_all():
        return mongo.db.users.find({})

    @staticmethod
    def update(user_id, update_dict):
        return mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_dict}
        )
    @staticmethod
    def delete(user_id):
        return mongo.db.users.delete_one({"_id": ObjectId(user_id)})