import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_DB_CONNECTION_STRING")
JWT_SECRET = os.getenv("JWT_SECRET")