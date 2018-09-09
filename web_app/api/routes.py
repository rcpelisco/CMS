from flask import Blueprint, jsonify, make_response, request
from models.models import User
from werkzeug import check_password_hash
import jwt
import datetime

module = Blueprint('api', __name__)

@module.route('login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, 
            {'www-Authenticate': 'Basic realm="Login required!"'})

    user = User()
    user.find_by_username(auth.username)

    if not user:
        return make_response('Could not verify', 401, 
            {'www-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.id, 
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secretparabibo')
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, 
            {'www-Authenticate': 'Basic realm="Login required!"'})