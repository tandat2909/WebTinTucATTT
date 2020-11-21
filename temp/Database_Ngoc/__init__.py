from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Team1.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


