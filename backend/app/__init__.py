from flask import Flask
from pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    
    mongo.init_app(app)

    # Blueprints (routes from express) here

    return app


def get_db():
    return mongo.db
