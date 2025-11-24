from flask import request, jsonify
from app.services.user_services import UserService


class UserController:

    @staticmethod
    def create():
        data = request.json
        user = UserService.save_user(data.name, data.email, data.password)
        if user:
            return jsonify(user), 201
        return jsonify({'message': 'User couldn\'t be registered'}), 405
    
    @staticmethod
    def get_all():
        users = UserService.get_users()
        return users
    
    @staticmethod
    def get_one_by_id(user_id):
        user = UserService.get_user_by_id(user_id)
        if user:
            return jsonify(user), 302
        return jsonify({'message': 'User not found'}), 404
    
    # @staticmethod
    # def get_one_by_username(username):
    #     user = UserService.get_user_by_username(username)
    #     if user:
    #         return jsonify(user), 302
    #     return jsonify({'message': 'User not found'}), 404
    
