import os

class Config:
    SECRET_KEY = 'clave-super-secreta'
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
