from flask import Flask
from webapp import config
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view='login_us'
listFormID ={'FormDelete':[]}
"""
    FormDelete= []

"""

