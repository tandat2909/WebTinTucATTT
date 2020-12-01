from flask_wtf import FlaskForm, form
from flask import flash, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, fields, validators
from wtforms.validators import DataRequired, ValidationError
import hashlib
from webapp.models import User, EStatus
from webapp import utils, models


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validators.length(1, 50, "Nhập tối 5 đến 50 ký tự")])
    password = PasswordField('Password', validators=[DataRequired(), validators.length(8, 50)])
    remember_me = BooleanField('Remember me', default=False)

    submit = SubmitField('Sign In')

    def __init__(self, *k, **kk):
        self._user = None  # for internal user storing
        super(LoginForm, self).__init__(*k, **kk)

    def validate(self):
        #print(self.username.data)
        self._user = User.query.filter(User.user_name == self.username.data,User.active == EStatus.Active).first()
        return super(LoginForm, self).validate()

    def validate_username(self, field):
        if self._user is None:
            flash("Invalid username or password", category='error')
            return

    def validate_password(self, field):
        if self._user:
            # flash(self._user.password + "\n" +self.password.data +"\n" +current_app.config.get('KEYPASS') + str( check_password_hash(self._user.password,self.password.data + current_app.config.get('KEYPASS'))))

            if not utils.check_password(self._user.password, self.password.data + current_app.config.get('KEYPASS')):
                flash("Invalid username or password", category='error')
                self._user = None
            return

    def get_user(self):
        return self._user
