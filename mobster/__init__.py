import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

my_project_path = 'C:\\Users\\crowd\\Desktop\\mobster\\'
on_server = False

if on_server:
	cf_path = '/etc/config.json'
else:
	cf_path = f'{my_project_path}\config.json'

with open(cf_path) as config_file:
	config = json.load(config_file)

app = Flask(__name__)

app.config['SECRET_KEY'] = config.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config.get('MOB_EMAIL')
app.config['MAIL_PASSWORD'] = config.get('MOB_PASS')
mail = Mail(app)

from mobster import routes 
