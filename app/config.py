import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
    DATABASE_URL = os.environ.get("DATABASE_URL")
    DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "app.db"))
    USING_POSTGRES = bool(os.environ.get("DATABASE_URL"))
    QUIZ_SIZE = 50
    MIN_RANGE = 50
    DEBUG = os.environ.get("DEBUG", "0").lower() in ("1", "true", "yes")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = not DEBUG
