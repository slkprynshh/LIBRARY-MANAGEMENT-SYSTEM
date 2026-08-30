import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "library_db")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    
    # Priority: 1. DATABASE_URL from env, 2. MySQL if USE_MYSQL=true, 3. SQLite default
    if os.getenv("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    elif os.getenv("USE_MYSQL", "false").lower() == "true":
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        sqlite_db_path = os.path.join(BASE_DIR, "library.db")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_lms_key_2026")
    JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", 24))
    FINE_PER_DAY = float(os.getenv("FINE_PER_DAY", 2))
    LOAN_PERIOD_DAYS = int(os.getenv("LOAN_PERIOD_DAYS", 14))
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

