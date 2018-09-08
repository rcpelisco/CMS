from flask import Blueprint, render_template
import requests
import json


module = Blueprint('patients', __name__, template_folder='templates')

@module.route('/')
def index():
    response = requests.get('http://localhost/api/patients/')
    return render_template('patients/index.html', data=json.loads(response.text)['patients'])

@module.route('/<patient>')
def show(patient):
    response = requests.get('http://localhost/api/patients/' + str(patient))
    return render_template('patients/show.html', patient=json.loads(response.text)['patient'])

@module.route('/create')
def create():
    return render_template('patients/create.html')