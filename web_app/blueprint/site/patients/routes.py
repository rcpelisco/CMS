from flask import Blueprint, render_template, url_for
from ..extra import get

import json

module = Blueprint('patients', __name__, template_folder='templates')

@module.route('/')
def index():
    response = get(url_for('api.patients.index'))
    return render_template('patients/index.html', 
        data=json.loads(response.text)['patients'])

@module.route('/<patient>')
def show(patient):
    response = get(url_for('api.patients.show', patient=patient))
    return render_template('patients/show.html', 
        patient=json.loads(response.text)['patient'])

@module.route('/create')
def create():
    return render_template('patients/create.html')
    
@module.route('/<patient>/add_record')
def add_record(patient):
    response = get(url_for('api.patients.show', patient=patient))
    return render_template('patients/add_record.html', 
        patient=json.loads(response.text)['patient'])
