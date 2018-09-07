from flask import Blueprint, jsonify

module = Blueprint('api', __name__)

@module.route('/')
def index():
    return jsonify(
        {
            'data': [
                {
                    'name': 'RC Pelisco',
                    'email': 'rcpelisco@gmail.com'
                },
                {
                    'name': 'Shim Bardo',
                    'email': 'shimbardo@gmail.com'
                },
            ]
        }
    )