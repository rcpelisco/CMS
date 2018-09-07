from flask import request, jsonify
from api.models.user import User
from functools import wraps
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'secretparabibo')
            current_user = User()
            current_user.find(data['public_id'])
        except:
            return jsonify({'message': 'Token is missing!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated
