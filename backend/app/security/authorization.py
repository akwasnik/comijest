from flask_jwt_extended import get_jwt, get_jwt_identity
from flask import jsonify
from .persmission import ROLE_PERMISSIONS

def has_permission(permission):
    claims = get_jwt()
    role = claims.get("role")
    return permission in ROLE_PERMISSIONS.get(role, set())


def has_any_permission(permissions):
    claims = get_jwt()
    role = claims.get("role")
    role_permissions = ROLE_PERMISSIONS.get(role, set())
    return any(p in role_permissions for p in permissions)


def permission_required_any(permissions):
    def wrapper(fn):
        def inner(*args, **kwargs):
            if not has_any_permission(permissions):
                return jsonify({"msg": "forbidden"}), 403
            return fn(*args, **kwargs)
        return inner
    return wrapper


def permission_required(permissions):
    def wrapper(fn):
        def inner(*args, **kwargs):
            if not has_permission(permissions):
                return jsonify({"msg": "forbidden"}), 403
            return fn(*args, **kwargs)
        return inner
    return wrapper


def can_acces_user(target_user_id):
    claims = get_jwt()
    role = claims.get("role")
    identity = get_jwt_identity()

    return role == "admin" or identity == target_user_id