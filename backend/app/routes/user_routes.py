from flask import Blueprint
from ..controllers.user_controllers import UserController

user_bp = Blueprint("users", __name__)

user_bp.post("/create")(UserController.create)
user_bp.get("/")(UserController.get_all)
user_bp.get("/<user_id>")(UserController.get_one)
user_bp.put("/<user_id>")(UserController.update)
user_bp.delete("/<user_id>")(UserController.delete)
