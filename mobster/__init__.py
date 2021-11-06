import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

with open('/etc/config.json') as config_file:
	config = json.load(config_file)

app = Flask(__name__)

try:
	with open('/etc/config.json') as config_file:
		config = json.load(config_file)
		
		app.config['SECRET_KEY'] = config.get('SECRET_KEY')
		app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
		app.config['MAIL_USERNAME'] = config.get('MOB_EMAIL')
		app.config['MAIL_PASSWORD'] = config.get('MOB_PASS')
else:
	app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
	app.config['MAIL_USERNAME'] = os.environ.get('MOB_EMAIL')
	app.config['MAIL_PASSWORD'] = os.environ.get('MOB_PASS')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

from mobster import routes 
