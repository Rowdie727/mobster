from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SHHH... This is a secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mobster_DB.db'
db = SQLAlchemy(app)

from mobster import routes 