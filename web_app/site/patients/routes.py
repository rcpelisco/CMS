from flask import Blueprint, render_template, url_for
from flask_login import login_required
from ..extra import get

import json

module = Blueprint('patients', __name__, template_folder='templates')

@module.route('/')
@login_required
def index():
    response = get(url_for('api.patients.index'))
    return render_template('patients/index.html', 
        data=json.loads(response.text)['patients'])

@module.route('/<patient>')
@login_required
def show(patient):
    response = get(url_for('api.patients.show', patient=patient))
    return render_template('patients/show.html', 
        patient=json.loads(response.text)['patient'])

@module.route('/create')
@login_required
def create():
    return render_template('patients/create.html')
    
@module.route('/<patient>/edit')
@login_required
def edit(patient):
    response = get(url_for('api.patients.show', patient=patient))
    return render_template('patients/edit.html', 
        patient=json.loads(response.text)['patient'])

@module.route('/<patient>/add_record')
@login_required
def add_record(patient):
    response = get(url_for('api.patients.show', patient=patient))
    return render_template('medical_records/create.html', 
        patient=json.loads(response.text)['patient'])
