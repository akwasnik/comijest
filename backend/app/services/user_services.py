from ..models.user import User
from ..repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def save_user(username, email, password):

        if UserRepository.find_by_email(email):
            return {"error": "Email already exists"}

        if UserRepository.find_by_username(username):
            return {"error": "Username already exists"}

        user = User(username, email, password)
        result = UserRepository.insert(user.to_dict())
        user.id = str(result.inserted_id)

        return user


    @staticmethod
    def get_users():
        users = UserRepository.find_all()
        return [User.from_mongo(u) for u in users]

    @staticmethod
    def get_user_by_id(user_id):
        data = UserRepository.find_by_id(user_id)
        return User.from_mongo(data)

    @staticmethod
    def update_user(user_id, data):
        user_data = UserRepository.find_by_id(user_id)
        if not user_data:
            return None

        user = User.from_mongo(user_data)

        # update fields
        if "username" in data:
            existing = UserRepository.find_by_username(data["username"])
            if existing and str(existing["_id"]) != user.id:
                return {"error": "Username already in use"}
            user.username = data["username"]

        if "email" in data:
            existing = UserRepository.find_by_email(data["email"])
            if existing and str(existing["_id"]) != user.id:
                return {"error": "Email already in use"}
            user.email = data["email"]

        if "password" in data:
            user.password = User(data["username"], data["email"], data["password"]).password

        UserRepository.update(user_id, user.to_dict())

        return user

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return None

        result = UserRepository.delete(user_id)
        return result.deleted_count > 0
