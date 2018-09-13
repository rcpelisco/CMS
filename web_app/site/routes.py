from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
module = Blueprint('site', __name__, template_folder='templates')

@module.route('/')
@login_required
def index():
    return render_template('index.html')

@module.route('/report')
@login_required
def report():
    return render_template('report.html')

@module.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))
    return render_template('login.html')

@module.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))
    return render_template('register.html')
