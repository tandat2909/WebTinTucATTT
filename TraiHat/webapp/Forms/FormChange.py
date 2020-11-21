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
    submit = SubmitField('Change')

    def __init__(self,*k,**kk):
      self._user=None #for internal user storing
      super(FormChangePassword,self).__init__(*k,**kk)
    def validate(self):
        self._user = models.User.query.get(current_user.user_id)
        print("_user change password",self._user.user_id)
        return super(FormChangePassword, self).validate()
    def validate_password(self,field):
        print('có chạy hàm val validate_password')
        if not self._user.is_authenticated:
            self._user=None
            return redirect(url_for('login',next=url_for('changepassword')))
        if not check_password_hash(self._user.password,self.password_Old.data):
            flash('Password old incorrect')
            self._user = None
            return False
        if self.password_New.data != self.password_Comfirm.data:
            flash("Mật khẩu mới và mật khẩu xác nận không trùng nhau")
            self._user = None
            return False
        if not check_password_hash(self.password,self.password_New.data):
            self._user = None
            flash('mật khẩu mới trùng mật khẩu cũ')
            return False
    def get_user(self):
        return self._user


