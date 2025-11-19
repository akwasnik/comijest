from flask import Flask
from flask_pymongo import PyMongo
from app.config import MONGO_URI

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = MONGO_URI


    mongo.init_app(app)

    try:
        print("Connection sucess Using DB:", mongo.db.name)
    except Exception as e:
        print("Connection failed:", e)
    #blueprints (routes) here
    return app
