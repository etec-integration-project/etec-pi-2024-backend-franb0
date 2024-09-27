import os
from datetime import datetime
from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the database and CORS
db = SQLAlchemy()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})  # Adjust the path as needed

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'createdAt': self.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': self.updatedAt.strftime('%Y-%m-%d %H:%M:%S')
        }

# Create a Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.environ['DATABASE_USERNAME']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}/{os.environ['DATABASE_NAME']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
cors.init_app(app)

# Create a blueprint for user routes
bp = Blueprint('users', __name__)

# Register a new user route
@bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not all(key in data for key in ('name', 'email', 'password')):
        return jsonify({'error': 'All fields (name, email, and password) are required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already in use. Please choose a different one.'}), 400

    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

# Login user route
@bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 400

# Get all users
@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Get user by ID
@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# Update user by ID
@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password = data['password']  # Plain text password (no hashing)
    db.session.commit()

    return jsonify(user.to_dict())

# Delete user by ID
@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

# Register the blueprint
app.register_blueprint(bp)

# Create database tables when the app starts
with app.app_context():
    db.create_all()

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3003)
