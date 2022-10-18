from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e550fec4dbc38d360d226ca689004f4e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site1.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)
from blogapp import routes