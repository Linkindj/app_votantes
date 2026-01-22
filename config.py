import os

class Config:
    SECRET_KEY = 'clave-super-secreta'
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("MYSQL_URL")
        .replace("mysql://", "mysql+pymysql://")
        + "?ssl=true"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
