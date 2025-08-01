from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Colums(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
