from flask_admin.contrib.sqla import ModelView
from WebApp.admin import admin
from WebApp import db
from WebApp.DataModels.AccountModels import Account
from flask_login import logout_user, current_user, login_required
from flask_admin import BaseView, expose
from flask import redirect,render_template

class AuthenticatedViewAdmin(ModelView):
    def is_accessible(self):
        try:
            if current_user.user_Name == "admin":
                return current_user.is_authenticated
            else:
                return False
        except:
            return False

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated

class UserView(AuthenticatedViewAdmin):
    @expose('/')
    def index(self):
        return render_template("admin/userview.html",user = current_user)

admin.add_view(ModelView(Account,db.session,name="user"))
#admin.add_view(UserView(Account,db.session,name="UserView"))
admin.add_view(LogoutView(name="Đăng xuất"))