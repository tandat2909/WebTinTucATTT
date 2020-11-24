from flask_wtf import FlaskForm, form
from flask import flash, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, fields, validators
from wtforms.validators import DataRequired, ValidationError
import hashlib
from webapp.models import User, EStatus
from webapp import utils, models

class delete(FlaskForm):
    ids = HiddenField('ids')
    submit = SubmitField('Sign In')
