from flask import g
from werkzeug.local import LocalProxy
from app import mongo

def get_db():
    """
    Returns the MongoDB database instance using global 'mongo' from app factory.
    """
    db = getattr(g, "_database", None)
    if db is None:
        g._database = mongo.db
    return g._database

db = LocalProxy(get_db)
