from flask import Blueprint, render_template

module = Blueprint('patients', __name__, template_folder='templates')

@module.route('/')
def index():
    data = {'header_text'}
    return render_template('patients/index.html')

@module.route('/<patient>')
def show(patient):
    return render_template('patients/show.html')

@module.route('/create')
def create():
    return render_template('patients/create.html')