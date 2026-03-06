import os

# Base directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "supersecretkey"

    # SQLite database file
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "newhiring.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Maximum upload size = 2MB
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024