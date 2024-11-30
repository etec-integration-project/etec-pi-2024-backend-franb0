# from flask import Blueprint, request, jsonify
# from .app import db
# from .models import User

# bp = Blueprint('users', __name__)

# @bp.route('/register', methods=['POST'])
# def register_user():
#     data = request.json

#     # Ensure name, email, and password are provided
#     if not all(key in data for key in ('name', 'email', 'password')):
#         return jsonify({'error': 'All fields (name, email, and password) are required'}), 400

#     # Check if email is unique
#     if User.query.filter_by(email=data['email']).first():
#         return jsonify({'error': 'Email already in use. Please choose a different one.'}), 400

#     # Create new user
#     new_user = User(name=data['name'], email=data['email'], password=data['password'])
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify(new_user.to_dict()), 201

# @bp.route('/users', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     return jsonify([user.to_dict() for user in users])

# @bp.route('/users/<int:id>', methods=['GET'])
# def get_user(id):
#     user = User.query.get_or_404(id)
#     return jsonify(user.to_dict())

# @bp.route('/users/<int:id>', methods=['PUT'])
# def update_user(id):
#     user = User.query.get_or_404(id)
#     data = request.json

#     # Update user fields
#     user.name = data.get('name', user.name)
#     user.email = data.get('email', user.email)
#     user.password = data.get('password', user.password)
#     db.session.commit()

#     return jsonify(user.to_dict())

# @bp.route('/users/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     user = User.query.get_or_404(id)
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message': 'User deleted'})
