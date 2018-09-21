from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import MetaData

naming_convention={
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
}

metadata = MetaData(naming_convention=naming_convention)

assets = Environment()

js = Bundle('js/core/jquery.min.js', 
    'js/core/popper.min.js',
    'js/core/bootstrap-material-design.min.js',
    'js/plugins/perfect-scrollbar.jquery.min.js',
    'js/plugins/moment.min.js',
    'js/plugins/jquery.serializejson.js',
    'js/plugins/jquery.validate.min.js',
    'js/plugins/jquery.bootstrap-wizard.js',
    'js/plugins/bootstrap-selectpicker.js',
    'js/plugins/bootstrap-datetimepicker.min.js',
    'js/plugins/jquery.dataTables.min.js',
    'js/plugins/bootstrap-tagsinput.js',
    'js/plugins/jasny-bootstrap.min.js',
    'js/plugins/chartist.min.js',
    'js/plugins/arrive.min.js',
    'js/plugins/bootstrap-notify.js',
    'js/material-dashboard.js',
    'js/plugins/jquery.getUrlParam.js',
    'js/plugins/sweetalert.min.js',
    'js/script.js',
    output='bundle/script.js')

css = Bundle('css/fonts.css',
    'css/font-awesome.min.css',
    'css/material-dashboard.min.css',
    'css/style.css',
    output='bundle/style.css')

db = SQLAlchemy(metadata=metadata)
login_manager = LoginManager()
login_manager.login_view = 'site.login'
