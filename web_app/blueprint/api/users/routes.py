from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User

module = Blueprint('api.users', __name__)

@module.route('/', methods=['GET'])
def index():
    user = User().all()

    return jsonify({'data': user})
    
@module.route('/', methods=['PUT', 'POST'])
def store():
    data = request.get_json()
    user = User()

    if request.method == 'PUT' and 'id' in data:
        user.find(data['id'])
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user.name = data['name']
    user.username = data['username']
    user.password = hashed_password

    return jsonify(user.save())

@module.route('/<patient>', methods=['GET'])
def show(patient):
    user = User().find(patient)
    return jsonify(user)

@module.route('/<patient>', methods=['DELETE'])
def delete(patient):
    user = User().delete(patient)
    return jsonify(user)
    