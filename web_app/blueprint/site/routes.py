from flask import Blueprint, render_template

module = Blueprint('site', __name__, template_folder='templates')

@module.route('/')
def index():
    return render_template('index.html')
