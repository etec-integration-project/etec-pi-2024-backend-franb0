import os
from datetime import datetime
from flask import Flask, Blueprint, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy, func
from flask_cors import CORS

# Create a Flask app
app = Flask(__name__)
app.secret_key = 'franb0_secretKey123#'

# Initialize the database and CORS
db = SQLAlchemy()
cors = CORS(app)

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

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image_url': self.image_url,
        }

class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.SmallInteger, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'product_id': self.product_id,
        }

class Support(db.Model):
    __tablename__ = 'support'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'email': self.email,
        }
    
class Cart(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date_time = db.session.query(func.current_timestamp()).scalar()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'date_time': self.date_time
        }

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.environ['DATABASE_USERNAME']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}/{os.environ['DATABASE_NAME']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
cors.init_app(app)

# Create a blueprint for user routes
bp = Blueprint('users', __name__)

# Register a new user route
@bp.route('/api/register', methods=['POST'])
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
@bp.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        session['name'] = user.name
        session['user_id'] = user.id
        return jsonify({'message': 'Login Succesfull'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 400
    
@app.route('/session-data')
def session_data():
    username = session.get('name', None)
    user_id = session.get('user_id', None)
    return jsonify({'name': username, 'user_id': user_id})
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('name', None)
    session.pop('user_id', None)
    return jsonify({'message': 'Logout Succesfull'}), 200

# Get all users
@bp.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Get user by ID
@bp.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# Update user by ID
@bp.route('/api/users/<int:id>', methods=['PUT'])
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
@bp.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@app.route('/api/rating/<int:product_id>', methods=['GET'])
def get_rating(product_id):
    ratings = Rating.query.filter_by(product_id=product_id).all()
    
    if not ratings:
        return jsonify({"error": "No ratings found for this product."}), 404

    total_ratings = sum(rating.rating for rating in ratings)
    average_rating = total_ratings / len(ratings)

    return jsonify({"rating": round(average_rating, 2)})

@app.route('/api/rate/<int:product_id>', methods=['POST'])
def rate_product(product_id):
    data = request.json
    rating_value = data['rating']
    
    if not (1 <= rating_value <= 5):
        return jsonify({"error": "Rating must be between 1 and 5."}), 400

    new_rating = Rating(rating=rating_value, product_id=product_id)
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({"message": "Rating added successfully!"}), 201

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/support', methods=['POST'])
def post_support():
    data = request.json
    description = data['description']
    email = data['email']
    
    if not description or not email:
        return jsonify({"error": "A description and Email should be provided."}), 400

    new_support = Support(description=description, email=email)
    db.session.add(new_support)
    db.session.commit()

    return jsonify({"message": "Support message added successfully!"}), 201

# Register the blueprint
app.register_blueprint(bp)

# Create database tables when the app starts
with app.app_context():
    db.create_all()

    products = [
        {"name": "Product 1", "price": 10, "image_url": "https://via.placeholder.com/150"},
        {"name": "Product 2", "price": 15, "image_url": "https://via.placeholder.com/150"},
        {"name": "Product 3", "price": 20, "image_url": "https://via.placeholder.com/150"},
    ]

    for product in products:
        existing_product = Product.query.filter_by(name=product["name"]).first()
        if not existing_product:
            new_product = Product(name=product["name"], price=product["price"], image_url=product["image_url"])
            db.session.add(new_product)

    db.session.commit()
    print("Products added succesfully")

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3003)
