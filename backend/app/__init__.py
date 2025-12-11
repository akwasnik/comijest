from flask import Flask
from .config import MONGO_URI
from .routes.user_routes import user_bp
from werkzeug.middleware.proxy_fix import ProxyFix
from pymongo import MongoClient
import certifi
def create_app():
    app = Flask(__name__)

    app.url_map.strict_slashes = False

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1
    )

    client = MongoClient(MONGO_URI)
    app.mongo = client["comijest"]

    try:
        print("Connection sucess Using DB:", app.mongo.db.name)
    except Exception as e:
        print("Connection failed:", e)
    app.register_blueprint(user_bp, url_prefix="/api/users")
    return app

app = create_app()