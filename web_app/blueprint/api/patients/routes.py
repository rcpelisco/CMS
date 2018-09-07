from flask import Blueprint, jsonify

module = Blueprint('api.patients', __name__)

@module.route('/', methods=['GET'])
def index():
    return jsonify({'data': [{'name': 'RC Pelisco', 'email': 'rcpelisco@gmail.com'},
        {'name': 'Shim Bardo', 'email': 'shimbardo@gmail.com'},]}
    )
    
@module.route('/', methods=['PUT', 'POST'])
def store():
    return jsonify({'name': 'RC Pelisco', 'email': 'rcpelisco@gmail.com'})

@module.route('/<patient>', methods=['DELETE'])
def delete(patient):
    return jsonify({'name': 'RC Pelisco', 'email': 'rcpelisco@gmail.com'})