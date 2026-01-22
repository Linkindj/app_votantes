import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-super-secreta")

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("MYSQL_URL") or
        "mysql+pymysql://root:@localhost/app_votantes"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
