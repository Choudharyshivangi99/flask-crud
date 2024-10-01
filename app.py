from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_swagger_ui import get_swaggerui_blueprint
from models import db, User, Item  # Importing models

# Flask app and extensions initialization
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecret'

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Path for swagger.json

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API Name"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Create database tables
with app.app_context():
    db.create_all()

# Authentication Blueprint
from auth import auth
app.register_blueprint(auth, url_prefix='/auth')

# CRUD Operations for Items
@app.route('/items', methods=['POST'])
@jwt_required()  # Protect this route
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], description=data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item created!"}), 201

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{"id": item.id, "name": item.name, "description": item.description} for item in items]), 200

@app.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()  # Protect this route
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify({"message": "Item updated!"}), 200

@app.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()  # Protect this route
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted!"}), 200

# Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Resource not found!"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"message": "Bad request!"}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Internal server error!"}), 500

if __name__ == '__main__':
    app.run(debug=True)
