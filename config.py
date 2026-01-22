from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin / doctor / patient

class Config:
    SECRET_KEY = "super-secret-key-123"
    SQLALCHEMY_DATABASE_URI = "sqlite:///hospital.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

