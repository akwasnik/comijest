from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from ..repositories.user_repository import UserRepository

class UserService:

    @staticmethod
    def create_user(username, email, password):
        if UserRepository.find_by_email(email):
            return None

        hashed = generate_password_hash(password)
        user = User(username, email, hashed)

        user_id = UserRepository.create(user)
        user.id = user_id
        return user

    @staticmethod
    def get_users():
        return UserRepository.find_all()

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.find_by_id(user_id)

    @staticmethod
    def update_user(user_id, data):
        if "password" in data:
            data["password"] = generate_password_hash(data["password"])

        return UserRepository.update(user_id, data)

    @staticmethod
    def delete_user(user_id):
        return UserRepository.delete(user_id)
