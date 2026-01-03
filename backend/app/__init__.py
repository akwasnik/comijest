from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from .config import JWT_SECRET, MONGO_URI
from .routes.user_routes import user_bp
from werkzeug.middleware.proxy_fix import ProxyFix
from pymongo import MongoClient
from .extensions import limiter, jwt


def create_app(testing=False):
    app = Flask(__name__)
    cors = CORS(
    app,
    resources={r"/api/*": {
        "origins": ["https://localhost:5000"],
        "allow_headers": ["Authorization", "Content-Type"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }},
    supports_credentials=True
    )
    app.url_map.strict_slashes = False

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1
    )

    #configuration for jwt and cookies
    if testing:
        app.config["JWT_SECRET_KEY"] = "test_secret"
    else:
        app.config["JWT_SECRET_KEY"] = JWT_SECRET
    
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    # app.config["JWT_COOKIE_SECURE"] = True         # HTTPS ONLY (PROD)
    app.config["JWT_COOKIE_SAMESITE"] = "None"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    # app.config["RATELIMIT_STORAGE_URI"] = "redis://redis:6379" #PROD
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt.init_app(app)

    client = MongoClient(MONGO_URI)

    app.mongo = client["comijest"]
    
    limiter.init_app(app)
    
    app.register_blueprint(user_bp, url_prefix="/api/users")

    return app

app = create_app()