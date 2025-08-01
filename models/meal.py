from database import db
from sqlalchemy.sql import func

class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    is_on_diet = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_on_diet': self.is_on_diet,
            'user_id': self.user_id
        }

def __repr__(self):
        return f"<Meal {self.name}>"