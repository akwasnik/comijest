from flask import Flask
from .extensions import mongo
from .config import MONGO_URI
from .routes.user_routes import user_bp
from pymongo import MongoClient
import certifi
def create_app():
    app = Flask(__name__)
    # app.config["MONGO_URI"] = MONGO_URI


    # mongo.init_app(app)
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    mongo = client["comijest"]

    try:
        print("Connection sucess Using DB:", mongo.db.name)
    except Exception as e:
        print("Connection failed:", e)
    app.register_blueprint(user_bp, url_prefix="/users")
    return app
