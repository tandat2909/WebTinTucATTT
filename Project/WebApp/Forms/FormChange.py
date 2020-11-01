
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import current_user

class ChangePasswordForm(FlaskForm):
    password_Old = PasswordField('password_Old', validators=[DataRequired()])
    password_New = PasswordField('password_New', validators=[DataRequired()])
    password_Comfirm = PasswordField('password_Comfirm', validators=[DataRequired()])
    submit = SubmitField('Change')

class ChangeAccountInformationForm(FlaskForm):
    userName_New = StringField('userName_New',validators=[DataRequired()])
    fullName_New = StringField('fullName_New', validators=[DataRequired()])
    email_New = StringField('email_New', validators=[DataRequired()])
    phoneNumber_New = StringField('phoneNumber_New', validators=[DataRequired()])
    pseudonym_New = StringField('pseudonym_New', validators=[DataRequired()])
    gender_New = StringField('gender_New', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Change')