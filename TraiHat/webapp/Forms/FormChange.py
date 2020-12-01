from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import current_user
#from werkzeug import check_password_hash,generate_password_hash
from flask import flash,abort,redirect,url_for
from webapp import app,db,models


class FormChangePassword(FlaskForm):
    password_Old = PasswordField('Password Old', validators=[DataRequired()])
    password_New = PasswordField('Password New', validators=[DataRequired()])
    password_Comfirm = PasswordField('Password Comfirm', validators=[DataRequired()])


