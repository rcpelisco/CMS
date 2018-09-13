from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from ..models.models import User
from ..models.schema import UserSchema

module = Blueprint('api.users', __name__)

users_schema = UserSchema(many=True)
user_schema = UserSchema()

@module.route('/', methods=['GET'])
def index():
    users = User.query.all()
    user_results, errors = users_schema.dump(users, many=True)
    return jsonify({'users': user_results})

@module.route('/<user>', methods=['GET'])
def show(user):
    user = User.query.get(user)
    if user is None:
        return jsonify({'message': 'User not found!'}), 400
    user_result, error = user_schema.dump(user)
    return jsonify({'user': user_result})

@module.route('/', methods=['PUT', 'POST'])
def store():
    json_data = request.get_json()
    user = User()
    message = 'User created'
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
        
    if 'id' in json_data:
        user = User.query.get(json_data['id'])
        message = 'User updated'

    if user is None:
        return jsonify({'message': 'User not found!'}), 400
    
    user.name = json_data['name']
    user.username = json_data['username']
    user.password = generate_password_hash(json_data['password'], method='sha256')
    user.save()

    user_result, errors = user_schema.dump(user)

    return jsonify({'message': message, 'user': user_result})

@module.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    user = User.query.filter_by(username=json_data['username']).first()
    if user and check_password_hash(user.password, json_data['password']):
        user_result, error = user_schema.dump(user)
        login_user(user)
        return jsonify({'message': 'User successfuly logged in', 'user': user_result})
    
    return jsonify({'message': 'Could not login'})

@module.route('/logout')
def logout():
    logout_user()
    return jsonify({'message': 'User logged out'})

@module.route('/<user>', methods=['DELETE'])
def delete(user):
    user = User.query.get(user)
    if user is None:
        return jsonify({'message': 'User not found!'}), 400
    user_data, errors = user_schema.dump(user)
    user_session = sessionmaker().object_session(user)
    user_session.delete(user)
    user_session.commit()
    return jsonify({'message': 'User deleted', 'user': user_data})
    