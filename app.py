from flask import Flask, request, jsonify
from models.meal import Meal
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet-api'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf8'), user.password):
                login_user(user)
                return jsonify({"message": "Logged in."})

    return jsonify({"message": "Invalid credentials."}), 401

@app.route('/logout', methods = ['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message":"Logged out."})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username and not password:
        return jsonify({"message":"Invalid credentials."}), 400
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exist."}), 409
    
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()) 

    new_user = User(username=username, password=hashed_password, role='user')

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"User registred!"})
    except:
        db.session.rollback()
        return jsonify({"message": "Internal error."}), 501

@app.route('/users/<int:id_user>', methods = ['GET'])
@login_required
def read_user(id_user):

    if current_user != id_user and current_user.role != 'admin':
        return jsonify({"message": "Forbidden"}), 403

    user = User.query.get(id_user)

    if user:
         return jsonify({"username": user.username, "id":user.id})
    
    return jsonify({"message":"User not found"}), 404
    
@app.route('/users/<int:id_user>/meals', methods=['POST'])
@login_required
def register_meal(id_user):

    if current_user.id != id_user:
        return jsonify({"message": "Forbidden"}), 403
    
    data = request.json
    name = data.get("name")
    description = data.get("description")
    datetime = data.get("datetime")
    is_on_diet = data.get("is_on_diet")

    if any(value is None for value in[name, description, datetime, is_on_diet]):
        return jsonify({"message":"Missing data required."}), 404
    
    try:
        new_meal = Meal(
            name=name,
            description=description,
            datetime=datetime,
            is_on_diet=is_on_diet,
            user_id=id_user
        )
        db.session.add(new_meal)
        db.session.commit()

        return jsonify({"message":"Meal registered"}), 200
    
    except:
        db.session.rollback()
        return jsonify({"message":"Internal error."}), 500

@app.route('/users/<int:id_user>/meals/<int:id_meal>/', methods=['GET'])
@login_required
def get_meal_details(id_user, id_meal):

    if current_user.id != id_user and current_user.role != 'admin':
        return jsonify({"message": "Forbidden"}), 403

    meals = Meal.query.filter_by(id=id_meal, user_id=id_user).first()

    if not meals:
        return jsonify({"message":"Meal not found."}), 404
    
    return jsonify(meals.to_dict()),200

@app.route('/users/<int:id_user>/meals', methods=['GET'])
def get_all_meal(id_user):

    if current_user.id != id_user and current_user.role != 'admin':
        return jsonify({"message": "Forbidden"}), 403

    meals = Meal.query.filter_by(user_id=id_user).all()

    if not meals:
        return jsonify({"message":"No meals found to this user"}), 404
    
    meal_list = [meal.to_dict() for meal in meals]

    return jsonify(meal_list),200

@app.route('/users/<int:id_user>', methods = ['DELETE'])
@login_required
def delete_user(id_user):

    if current_user.role != "admin":
        return jsonify({"message":"Operation not permited"}),403
    
    if id_user == current_user.id:
        return jsonify({"message":"User deletion not permited"}),403   
    
    user_to_delete = db.session.get(User, id_user)

    if not user_to_delete:
        return jsonify({"message": f"User with id {id_user} not found."}), 404
    
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({"message":f"User {id_user} deleted succefully"}),200
    
    except:
        db.session.rollback()
        return jsonify({"message":"Internal error."}), 500
    
@app.route('/users/<int:id_user>/meals/<int:id_meal>/', methods = ['DELETE'])
@login_required
def delete_meal(id_user, id_meal):

    if current_user.id != id_user and current_user.role != "admin":
        return jsonify({"message":"Operation not permited"}),403
    
    meal_to_delete = Meal.query.filter_by(id=id_meal, user_id=id_user).first()
    
    if not meal_to_delete:
        return jsonify({"message": "Meal not found."}), 404
    
    try:
        db.session.delete(meal_to_delete)
        db.session.commit()
        return jsonify({"message":"Meal deleted succefully"}),200
    
    except:
        db.session.rollback()
        return jsonify({"message":"Internal error."}), 500
     

@app.route('/users/<int:id_user>/meals/<int:id_meal>', methods = ['PUT'])
@login_required
def update_meal(id_user, id_meal):

    meal_to_update = Meal.query.filter_by(id=id_meal, user_id=id_user).first()

    data = request.json

    try:
        if "name" in data:
            meal_to_update.name = data["name"]

        if "description" in data:
            meal_to_update.description = data["description"]

        if "is_on_diet" in data:
            meal_to_update.is_on_diet = data["is_on_diet"]

        db.session.commit()
        return jsonify({"message":"Meal updated"})
    
    except:
        db.session.rollback()
        print("Error updating meal.")
        return({"message":"Internal error"}), 500

if __name__ == '__main__':
    app.run(debug=True)