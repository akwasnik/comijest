from flask import request, jsonify
from ..services.user_services import UserService


class UserController:

    @staticmethod
    def create():
        data = request.json
        user = UserService.save_user(
            data.get("username"),
            data.get("email"),
            data.get("password")
        )

        if isinstance(user, dict) and "error" in user:
            return jsonify(user), 400

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }), 201


    @staticmethod
    def get_all():
        users = UserService.get_users()
        return jsonify([
            {"id": u.id, "username": u.username, "email": u.email}
            for u in users
        ]), 200


    @staticmethod
    def get_one_by_id(user_id):
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }), 200


    @staticmethod
    def update_user(user_id):
        data = request.json
        user = UserService.update_user(user_id, data)

        if user is None:
            return jsonify({"message": "User not found"}), 404

        if isinstance(user, dict) and "error" in user:
            return jsonify(user), 400

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }), 200

    @staticmethod
    def delete_user(user_id):
        deleted = UserService.delete_user(user_id)

        if deleted is None:
            return jsonify({"message": "User not found"}), 404

        if deleted:
            return jsonify({"message": "User deleted successfully"}), 200

        return jsonify({"message": "User could not be deleted"}), 400
