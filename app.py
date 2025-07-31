from flask import Flask, request, jsonify
from models.meal import Meal
from models.user import User
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet-api'

db.init_app(app)

@app.route('/user/meal', methods=['POST'])
def register_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    datetime = data.get("datetime")
    is_on_diet = data.get("is_on_diet")

    if any(value is None for value in[name, description, datetime, is_on_diet]):

        return jsonify({"message":"Missing data required."}), 404
    
    return jsonify({"message":"Meal registered succefully."})

@app.route('/meal/<int:id>', methods=['GET'])
def get_meal(id):
    meal = Meal.query.get(id)

    if meal:
        return jsonify({
            "username":meal.username,
            "description":meal.description,
            "datetime": meal.datetime,
            "is_on_diet": meal.is_on_diet
        })
    return jsonify({"message":"Meal not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

