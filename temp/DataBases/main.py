from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="mssql+pymssql://sa:123@127.0.0.1:1434/master"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "username"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String,  nullable=False)

class product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer,primary_key= True)
    ProductName = db.Column(db.String,nullable=False)

db.create_all()

pro = product(id=3,ProductName = "kádấd")
user = User(id = 1,username="dat",email="vutandat@gmail.com")
db.session.add(pro)
db.session.add(user)
db.session.commit()
print(User.query.filter_by(username='dat').first())
