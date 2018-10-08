from flask import Blueprint, render_template, url_for
from flask_login import login_required, login_fresh
from ..extra import get

import json

module = Blueprint('users', __name__, template_folder='templates')

@module.route('/')
def index():
    return render_template('users/index.html')

@module.route('/<user>')
def show(user):
    response = get(url_for('api.users.show', user=user))
    return render_template('users/show.html', 
        user=json.loads(response.text)['user'])

@module.route('/create')
def create():
    return render_template('users/create.html')

    
@module.route('/<user>/edit')
@login_required
def edit(user):
    response = get(url_for('api.users.show', user=user))
    return render_template('users/edit.html', 
        user=json.loads(response.text)['user'])