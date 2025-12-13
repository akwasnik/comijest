from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controllers.user_controllers import UserController

user_bp = Blueprint("users", __name__)

user_bp.post("/create")(UserController.create)
user_bp.get("/")(jwt_required()(UserController.get_all))
user_bp.get("/<user_id>")(jwt_required()(UserController.get_one))
user_bp.put("/<user_id>")(jwt_required()(UserController.update))
user_bp.delete("/<user_id>")(jwt_required()(UserController.delete))
user_bp.post("/login")(UserController.login)
