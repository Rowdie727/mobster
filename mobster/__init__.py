import json
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

my_project_path = 'C:\\Users\crowd\Desktop\mobties'
on_server = True

if on_server:
	config_path = '/etc/config.json'
else:
	config_path = f'{my_project_path}\config.json'

with open(config_path) as config_file:
	config = json.load(config_file)

app = Flask(__name__)

app.config['SECRET_KEY'] = config.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
migrate = Migrate(app, db)
from mobster import routes 
