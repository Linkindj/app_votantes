from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'   # 👈 MUY IMPORTANTE

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Votante(db.Model):
    __tablename__ = 'votantes'  # 👈 MUY IMPORTANTE

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    cedula = db.Column(db.String(20), unique=True)
    edad = db.Column(db.String(20))
    ocupacion=db.Column(db.String(30),unique=True)
    telefono=db.Column(db.String(20))
    punto_vacunacion = db.Column(db.String(100))
    mesa_vacunacion = db.Column(db.String(50))
    lider_referencia=db.Column(db.String(50))
    lider_id = db.Column(db.Integer, db.ForeignKey('lider.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    lider = db.relationship('Lider', backref='votantes')
    

class lugarVotacion(db.Model):
    __tablename__ = 'lugar_votacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)


class Lider(db.Model):
    __tablename__ = 'lider'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
