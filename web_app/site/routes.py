from flask import Blueprint, render_template

module = Blueprint('site', __name__, template_folder='templates')

@module.route('/')
def index():
    return render_template('index.html')

@module.route('/report')
def report():
    return render_template('report.html')

@module.route('/login')
def login():
    return render_template('login.html')

@module.route('/register')
def register():
    return render_template('register.html')
