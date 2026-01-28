import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_DB_CONNECTION_STRING")
JWT_SECRET = os.getenv("JWT_SECRET")

MODEL_DIR = os.getenv("MODEL_DIR")
MODEL_MAX_LENGTH = int(os.getenv("MODEL_MAX_LENGTH", "64"))

TRANSLATION_PROVIDER = os.getenv("TRANSLATION_PROVIDER", "libre")
LIBRE_TRANSLATE_URL = os.getenv("LIBRE_TRANSLATE_URL")
