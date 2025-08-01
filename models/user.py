from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')
    meals = db.Relationship('Meal', backref='owner', lazy='dynamic', cascade='all, delete-orphan') 
