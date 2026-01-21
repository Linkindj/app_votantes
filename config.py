class Config:
    SECRET_KEY = 'clave-super-secreta'
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:@localhost/app_votantes'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False