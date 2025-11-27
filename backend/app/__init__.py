from flask import Flask
from .extensions import mongo
from app.config import MONGO_URI
from .routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = MONGO_URI


    mongo.init_app(app)

    try:
        print("Connection sucess Using DB:", mongo.db.name)
    except Exception as e:
        print("Connection failed:", e)
    app.register_blueprint(user_bp, url_prefix="/users")
    return app
