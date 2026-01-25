from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
import sys

MONGO_URI = os.getenv("MONGO_DB_CONNECTION_STRING")
DB_NAME = "comijest"

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def fail(msg):
    print(f"failed creating Admin: {msg}")
    sys.exit(1)

def main():
    if not MONGO_URI:
        fail("MONGO_URI not set")

    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        fail("ADMIN_EMAIL or ADMIN_PASSWORD not set")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users = db.users

    #Don't create admin if exists
    if users.find_one({"email": ADMIN_EMAIL}):
        print("ℹ️ Admin already exists — skipping")
        return

    admin = {
        "username": ADMIN_USERNAME,
        "email": ADMIN_EMAIL,
        "password": generate_password_hash(ADMIN_PASSWORD),
        "role": "admin",
        "created_at": datetime.utcnow()
    }

    users.insert_one(admin)
    print("Admin user created")

if __name__ == "__main__":
    main()
