from flask import request, jsonify, current_app as app
from .app import db
from .models import User

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json

    # Verificar que el nombre de usuario y la contraseña estén presentes
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Todos los campos (nombre, correo y contraseña) son obligatorios'}), 400

    # Verificar que el nombre de usuario sea único
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El correo ya está en uso. Por favor elija uno diferente.'}), 400

    # Crear un nuevo usuario
    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.name = data['name']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})
