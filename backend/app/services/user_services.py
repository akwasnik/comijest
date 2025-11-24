from ..models.user import User

class UserService:

    @staticmethod
    def save_user(username, email, password):
        if (User.find_by_email(email)):
            return None
        if (User.find_by_username):
            return None
        user = User(username, email, password)
        user.save()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.find_by_id(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        return User.find_by_username(username)
    
    @staticmethod
    def get_user_by_email(email):
        return User.find_by_email(email)
    
    @staticmethod
    def get_users():
        users = User.collection.find({})
        return [User.from_mongo(u) for u in users]