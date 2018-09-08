from flask import Flask
from extension import db

from api.routes import module
from api.users.routes import module
from api.patients.routes import module
from api.medical_records.routes import module

from site.routes import module
from site.users.routes import module
from site.patients.routes import module

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretparabibo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cms'

db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

app.register_blueprint(api.routes.module, url_prefix='/api')
app.register_blueprint(api.users.routes.module, url_prefix='/api/users')
app.register_blueprint(api.patients.routes.module, url_prefix='/api/patients')
app.register_blueprint(api.medical_records.routes.module, url_prefix='/api/medical_records')

app.register_blueprint(site.routes.module, url_prefix='/')
app.register_blueprint(site.patients.routes.module, url_prefix='/patients')
app.register_blueprint(site.users.routes.module, url_prefix='/users')
