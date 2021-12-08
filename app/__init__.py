# this is the file for app init

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import logging
from logging.handlers import TimedRotatingFileHandler

# app init
app = Flask(__name__, template_folder='templates')

# database configuation
app.config.from_object('config')
db = SQLAlchemy(app)

# bootstrap configuation
bootstrap = Bootstrap(app)

# login configuation
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# login_manager.session_protection = "strong"


# database migration
Migrate(app, db)

csrf = CSRFProtect()
csrf.init_app(app)

logging.basicConfig(level=logging.DEBUG)

handler = logging.FileHandler('flask.log')
handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter('[%(asctime)s][%(filename)s-%(funcName)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

from app import model, login, views, okr_function, group_function
# export FLASK_APP="__init__"
