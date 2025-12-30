from flask_jwt_extended import jwt_required

def protected():
    return jwt_required()