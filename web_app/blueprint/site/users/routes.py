from flask import Blueprint, render_template

module = Blueprint('users', __name__, template_folder='templates')

@module.route('/')
def index():
    data = {'header_text'}
    return render_template('users/index.html')

@module.route('/<user>')
def show(patient):
    return render_template('users/show.html')

@module.route('/create')
def create():
    return render_template('users/create.html')