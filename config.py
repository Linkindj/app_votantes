import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-super-secreta")

    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_URL")

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ca": "/etc/ssl/certs/ca-certificates.crt"
            }
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False