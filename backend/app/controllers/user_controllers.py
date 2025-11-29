from flask import request, jsonify
from ..services.user_services import UserService

class UserController:

    @staticmethod
    def create():
        data = request.json
        user = UserService.create_user(
            data["username"],
            data["email"],
            data["password"]
        )
        if not user:
            return jsonify({"message": "User already exists"}), 409

        return jsonify({"id": user.id, "username": user.username}), 201

    @staticmethod
    def get_all():
        users = UserService.get_users()
        return jsonify([u.to_dict() for u in users]), 200

    @staticmethod
    def get_one(user_id):
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify(user.to_dict()), 200

    @staticmethod
    def update(user_id):
        data = request.json
        updated = UserService.update_user(user_id, data)
        return jsonify({"message": updated}), 200

    @staticmethod
    def delete(user_id):
        UserService.delete_user(user_id)
        return jsonify({"message": "User deleted"}), 200
