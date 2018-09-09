from flask import Flask
from extension import db

from filters import format_date, format_datetime, format_age

from api.routes import module
from api.users.routes import module
from api.patients.routes import module
from api.medical_records.routes import module
from api.face_recognition.routes import module

from site.routes import module
from site.users.routes import module
from site.patients.routes import module
from site.medical_records.routes import module

from face_recognition.routes import module

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretparabibo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cms'
app.config["JSON_SORT_KEYS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.commit()

app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['date'] = format_date
app.jinja_env.filters['age'] = format_age

app.register_blueprint(api.routes.module, url_prefix='/api')
app.register_blueprint(api.users.routes.module, url_prefix='/api/users')
app.register_blueprint(api.patients.routes.module, url_prefix='/api/patients')
app.register_blueprint(api.medical_records.routes.module, url_prefix='/api/medical_records')
app.register_blueprint(api.face_recognition.routes.module, url_prefix='/api/face_recognition')

app.register_blueprint(site.routes.module, url_prefix='/')
app.register_blueprint(site.users.routes.module, url_prefix='/users')
app.register_blueprint(site.patients.routes.module, url_prefix='/patients')
app.register_blueprint(site.medical_records.routes.module, url_prefix='/medical_records')

app.register_blueprint(face_recognition.routes.module, url_prefix='/face_recognition')
