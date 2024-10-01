from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from models import User, db

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()
jwt = JWTManager()

# User Registration
@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debugging statement
        if not data:
            return jsonify({"message": "No input data provided"}), 400
        if 'username' not in data or 'password' not in data:
            return jsonify({"message": "Username and password required"}), 400
        
        # Check if the user already exists
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return jsonify({"message": "Username already exists"}), 400
        
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        print(f"Hashed password: {hashed_password}")  # Debugging statement
        
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "User registered successfully!"}), 201
    
    except Exception as e:
        print(f"Error occurred: {e}")  # Debugging error message
        return jsonify({"message": "An error occurred during registration."}), 500

# User Login
@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"Received login data: {data}")  # Debugging statement
        user = User.query.filter_by(username=data['username']).first()

        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.username)
            print(f"Access token created: {access_token}")  # Debugging statement
            return jsonify({"token": access_token}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    
    except Exception as e:
        print(f"Error occurred during login: {e}")  # Debugging error message
        return jsonify({"message": "An error occurred during login."}), 500