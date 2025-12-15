from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from ..exceptions.user_exceptions import EmailTakenError, InvalidPasswordOrEmail, SamePasswordError, UsernameTakenError
from ..models.user import User
from ..repositories.user_repository import UserRepository

class UserService:

    @staticmethod
    def create_user(username, email, password):
        if UserRepository.find_by_email(email):
            return None
        if UserRepository.find_by_username(username):
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
        if "username" in data:
            existing = UserRepository.find_by_username(data["username"])
            if existing and existing.id != user_id:
                raise UsernameTakenError()
        if "email" in data:
            existing = UserRepository.find_by_email(data["email"])
            if existing and existing.id != user_id:
                raise EmailTakenError()
        if "password" in data:
            same_password = check_password_hash(UserRepository.find_by_id(user_id).password, data["password"])
            if same_password:
                raise SamePasswordError()
            data["password"] = generate_password_hash(data["password"])

        return UserRepository.update(user_id, data)

    @staticmethod
    def delete_user(user_id):
        return UserRepository.delete(user_id)
    
    @staticmethod
    def login_user(email, password):
        user = UserRepository.find_by_email_for_login(email)
        if user:
            if check_password_hash(user.password, password):
                return create_access_token(identity=user.id, additional_claims={"role": user.role})
        raise InvalidPasswordOrEmail