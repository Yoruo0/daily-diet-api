from database import db

class User(db.Model):
    username = db.Colums(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    id = db.Column(db.Integer, primary_key=True)