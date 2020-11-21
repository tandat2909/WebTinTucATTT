from functools import wraps
import hashlib
from flask import url_for, request, redirect, render_template, session, abort, Response, g, flash, current_app
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_login import login_user, login_required
from markupsafe import Markup
from wtforms import validators, PasswordField, HiddenField, StringField, Field, widgets, ValidationError
from wtforms.compat import text_type
from wtforms.widgets.core import Input
from webapp import app,db,models,login
from flask_login import login_user,current_user,logout_user,AnonymousUserMixin
from webapp.models import User
#from webapp.admin.routeAdmin import *
from webapp.Forms.FormLogin import LoginForm
from webapp.Forms import FormChange
from werkzeug.security import generate_password_hash

def login_required_Admin(f):
    '''
    bắt buộc đăng nhập với quyền admin
    :param f: function
    :return:
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or not current_user.is_authenticated or current_user.user_role_id != models.EUserRole.admin.value:
            flash('Please login to access this page.')
            return redirect(url_for('loginAdmin', next=request.url_rule))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/admin/logout")
@app.route("/user/logout")
@login_required
def logout():
    '''
    đăng xuất
    :return:
    '''
    logout_user()

    return redirect(url_for('login'))


@app.route("/user/login",methods=["GET","POST"])
def login():
    '''
    login cho trang user
    :return:
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        next_url = request.args.get('next')
        if user and user.active == models.EStatus.Active and user.user_role_id != models.EUserRole.anonymous:
            flash("Login Success", category='success')
            login_user(user= user)
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index_user'))

        logout_user()
        if user:
            flash("Invalid username or password", category='error')
            user = None
    return render_template('login.html', form=form, title="Login User",action = "login" )

@app.route("/admin/login",methods=["GET","POST"])
def loginAdmin():
    '''
    login cho trang admin
    :return:
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        next_url = request.args.get('next')
        if user and user.active == models.EStatus.Active and user.user_role_id == models.EUserRole.admin.value:
            login_user(user)
            flash("Login Success", category='success')
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index_admin'))

        logout_user()
        if user:
            flash("Invalid username or password", category='error')
            user = None

    return render_template('login.html',form = form,title = 'Login Admin',action = 'loginAdmin')



@app.route("/user/profile")
@app.route("/admin/profile")
@login_required
def profile():
    '''
    hiển thị thong tin chi tiết của user
    :return:
    '''
    if current_user.user_role.id == models.EUserRole.admin.value:
        id = request.args.get("id")
        return id
    return str(current_user.id)

@app.route("/user/bloglist")
@app.route("/admin/bloglist")
@login_required
def bloglist():
    '''
    admin: hiển thị tất cả bài viết của user
    user: hiển bài viết của user đó
    :return:
    '''
    if current_user.user_role.id == models.EUserRole.admin.value:
        listblog = models.QL_BaiViet.query.all()
        print(listblog)
        return render_template('admin/index.html',listblog = listblog)
    return str(current_user.id)

    #return render_template('bloglist.html',listblock = listblog)

@app.route("/user/blog")
@app.route("/admin/blog")
def bloguser():
    '''
    hiển thị detail blog
    dùng template admin (blog.html)
    :return:
    '''
    if current_user.user_role.id == models.EUserRole.admin.value:
        pass
    return str(current_user.id)

    #return render_template('bloglist.html',listblock = listblog)

@app.route('/admin')
@login_required_Admin
def index_admin():
    '''
    hiển thị biểu đồ or bài viết
    :return:
    '''

    return render_template('admin/index.html')

@app.route('/admin/userlist')
@login_required_Admin
def userlist():
    '''
    hiển thị tất cả user trừ tài khoản admin hiện tại
    :return:
    '''
    #test lấy dữ liệu
    listuser = models.User.query.all()
    print(listuser)
    return render_template('admin/UserList.html',title = "User List" ,listuser = listuser)

@app.route('/user')
@login_required
def index_user():
    '''
    hiển thị list bài viết của user đây
    :return:
    '''
    return render_template('page.html')

@app.route('/changepw',methods=["POST","GET"])
@login_required
def changepassword():
    '''
    thay đổi password
    chưa làm : mã hóa mật khẩu
    :return:
    '''
    form = FormChange.FormChangePassword()
    if form.validate_on_submit():
        user = form.get_user()
        if user:
            user.password = generate_password_hash(form.password_Comfirm.data)
            print(user.user_name,user.password)
            db.Session.add(user)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('ChangePassword.html',form=form)

@app.route('user/delete/blog',methods=["POST"])
@app.route('admin/delete/blog',methods=["POST"])
@login_required
def deleteBlog():
    '''
    user: delete blog user đó
    admin: delete all blog
    nhận id bài viết
    gửi lên dạng post form có csrf
    :return:
    '''
    pass

@app.route('admin/delete/user',methods=["POST"])
@login_required_Admin
def deleteUser():
    '''
    xóa user bằng cách cho trường active của user đó  = False or user.active = models.EStatus.InActive
    gửi yêu cầu dạng form có csrf

    :return:
    '''
    pass
#================== làm cho anonymous ========================================


@app.route("/")
def index():
    '''
    hiểm thị list các blog xắp xếp theo time giảm dần
    :return:
    '''
    return render_template("index.html")

@app.route('/blog')
def blog():
    '''
        blog detail
        kế thừa page.html tạo trang mới để hiển thị nội dung blog
    :return:
    '''
    pass

@app.route("/about")
def about():
    '''
    còn time thì làm hiển thị thông tin của nhóm mình ở đây
    :return:
    '''
    return render_template('page.html')

@app.route("/contact")
def contact():
    '''
    làm không làm cũng đc
    :return:
    '''
    return render_template('page.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html',code = 404, ms = 'Error Pagee'), 404


if __name__ == "__main__":

   # app.run(debug=True,host="192.168.1.7",port="5000")
    app.run(debug=True)