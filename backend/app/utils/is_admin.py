from flask_jwt_extended import jwt_required, get_jwt
from flask import jsonify

def admin_required():
    def wrapper(fn):
        return jwt_required()(lambda *args, **kwargs: _check_admin(fn, *args, **kwargs))
    return wrapper

def _check_admin(fn, *args, **kwargs):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return fn(*args, **kwargs)
