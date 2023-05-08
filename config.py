import os

class Config:
    SECRET_KEY = os.urandom(12).hex()
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False