from flask import Flask
from .config import JWT_SECRET, MONGO_URI
from .routes.user_routes import user_bp
from werkzeug.middleware.proxy_fix import ProxyFix
from pymongo import MongoClient
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    app.url_map.strict_slashes = False

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1
    )

    #configuration for jwt
    app.config["JWT_SECRET_KEY"] = JWT_SECRET
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    jwt = JWTManager(app)

    client = MongoClient(MONGO_URI)

    app.mongo = client["comijest"]

    try:
        print("Connected to DB")
    except Exception as e:
        print("Connection failed:", e)
    
    app.register_blueprint(user_bp, url_prefix="/api/users")

    return app

app = create_app()