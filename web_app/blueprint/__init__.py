from flask import Flask
from extension import mysql

from api.routes import module
from api.patients.routes import module
from api.users.routes import module

from site.routes import module
from site.patients.routes import module
from site.users.routes import module

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretparabibo'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cms'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)

app.register_blueprint(api.routes.module, url_prefix='/api')
app.register_blueprint(api.patients.routes.module, url_prefix='/api/patients')
app.register_blueprint(api.users.routes.module, url_prefix='/api/users')

app.register_blueprint(site.routes.module)
app.register_blueprint(site.patients.routes.module, url_prefix='/patients')
app.register_blueprint(site.users.routes.module, url_prefix='/users')

