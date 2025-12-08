from flask import request, jsonify
from ..schemes.user_scheme import UserSchema, UpdateUserSchema
from ..services.user_services import UserService
from ..exceptions.user_exceptions import EmailTakenError, SamePasswordError, UsernameTakenError
from marshmallow import ValidationError

class UserController:

    @staticmethod
    def create():
        try:
            data = UserSchema().load(request.get_json())
        except ValidationError as err:
            return {"errors": err.messages}, 400
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
        try:
            data = UpdateUserSchema().load(request.get_json())
            data = request.json
            updated = UserService.update_user(user_id, data)
            return jsonify({"message": updated}), 200
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except UsernameTakenError as err:
            return jsonify({"error": "Username already taken"}), 409
        except EmailTakenError as err:
            return jsonify({"error": "Email already taken"}), 409
        except SamePasswordError as err:
            return jsonify({"error": "New password cannot be the same as the old one"}), 400

    @staticmethod
    def delete(user_id):
        UserService.delete_user(user_id)
        return jsonify({"message": "User deleted"}), 200
