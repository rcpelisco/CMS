from flask import Blueprint, render_template, url_for, make_response
from ..extra import get
import pdfkit
import json

module = Blueprint('medical_records', __name__, template_folder='templates')

@module.route('/')
def index():
    pass

@module.route('/<medical_record>')
def show(patient):
    response = get('/patients/' + str(patient))
    return render_template('patients/show.html', 
        patient=json.loads(response.text)['patient'])

@module.route('/<medical_record>/edit')
def edit(medical_record):
    response = get(url_for('api.medical_records.show', medical_record=medical_record))
    return render_template('medical_records/edit.html', 
        medical_record=json.loads(response.text)['medical_record'])

@module.route('/create')
def create():
    return render_template('patients/create.html')
    
@module.route('/<medical_record>/add_record')
def add_record(patient):
    response = get('/patients/' + str(patient))
    return render_template('patients/add_record.html', 
        patient=json.loads(response.text)['patient'])


@module.route('/<medical_record>/print', methods=['GET'])
def purintu(medical_record):
    options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '1in',
        'margin-bottom': '0.5in',
        'margin-left': '1in',
    }
    response_data = get(url_for('api.medical_records.show', medical_record=medical_record))
    template = render_template('medical_records/print.html', medical_record=json.loads(response_data.text)['medical_record'])
    pdf = pdfkit.from_string(template, False, options=options)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response
