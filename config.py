import os

class Config:
    SECRET_KEY = 'clave-super-secreta'
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_URL") .replace(
        "mysql://", "mysql+pymysql://")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print("MYSQL_URL:", os.getenv("MYSQL_URL"))