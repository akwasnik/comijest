from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, set_refresh_cookies, unset_jwt_cookies

from ..security.authorization import can_access_user
from ..schemes.user_scheme import UserLoginSchema, UserSchema, UpdateUserSchema
from ..services.user_services import UserService
from ..exceptions.user_exceptions import EmailTakenError, InvalidPasswordOrEmail, SamePasswordError, UsernameTakenError
from marshmallow import ValidationError

class UserController:

    @staticmethod
    def create():
        try:
            data = UserSchema().load(request.get_json())
        
            user = UserService.create_user(
                data["username"],
                data["email"],
                data["password"]
            )
            if not user:
                return jsonify({"message": "User already exists"}), 409
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        return jsonify({"id": user.id, "username": user.username}), 201


    def login():
        try:
            data = UserLoginSchema().load(request.get_json())

            access, refresh = UserService.login_user(
                data["email"], data["password"]
            )

            response = jsonify({"msg": "logged in"})

            set_access_cookies(response, access)
            set_refresh_cookies(response, refresh)

            return response, 200
        except InvalidPasswordOrEmail:
            return jsonify({"error": "Invalid email or password"}), 401
    
    @staticmethod
    def get_all():
        users = UserService.get_users()
        return jsonify([u.to_public_dict() for u in users]), 200

    @staticmethod
    def get_one(user_id):
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        if not can_access_user(user_id):
            return {"msg": "forbidden"}, 403
        return jsonify(user.to_public_dict()), 200
    
    
    @staticmethod
    @jwt_required()
    def get_me():
        user_id = get_jwt_identity()
        user = UserService.get_user_by_id(user_id)

        if not user:
            return {"msg": "User not found"}, 404

        return user.to_public_dict(), 200

    @staticmethod
    def update(user_id):
        if not can_access_user(user_id):
            return jsonify({"msg": "forbidden"}), 403
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

    @staticmethod
    @jwt_required(refresh=True)
    def refresh():
        user_id = get_jwt_identity()
        claims = get_jwt()
    
        new_access = create_access_token(
            identity=user_id,
            additional_claims={"role": claims.get("role")}
        )
    
        response = jsonify({"msg": "token refreshed"})
        set_access_cookies(response, new_access)
    
        return response, 200
    
 
    @staticmethod
    def logout():
        response = jsonify({"msg": "logout"})
        unset_jwt_cookies(response)
        return response, 200
    
    @staticmethod
    @jwt_required()
    def update_me():
        user_id = get_jwt_identity()
        data = request.get_json()
        UserService.update_user(user_id, data)
        return {"message": True}, 200
    
    @staticmethod
    @jwt_required()
    def get_me():
        user_id = get_jwt_identity()
        user = UserService.get_user_by_id(user_id)
    
        if not user:
            return {"msg": "User not found"}, 404
    
        return user.to_public_dict(), 200