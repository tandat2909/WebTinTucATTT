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
from webapp import app, db, models, login,jinja_filters
from flask_login import login_user, current_user, logout_user, AnonymousUserMixin
from webapp.models import User
# from webapp.admin.routeAdmin import *
from webapp.Forms.FormLogin import LoginForm
from webapp.Forms import FormChange
from werkzeug.security import generate_password_hash


def login_required_Admin(f):
    """
    bắt buộc đăng nhập với quyền admin
    :param f: function
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or not current_user.is_authenticated or current_user.user_role_id != models.EUserRole.admin.value:
            flash('Please login to access this page.')
            return redirect(url_for('login_admin', next=request.url_rule))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/admin/logout")
@app.route("/user/logout")
@login_required
def logout():
    """
    đăng xuất
    :return:
    """
    logout_user()
    return redirect(url_for('login_us'))


@app.route("/user/login", methods=["GET", "POST"])
def login_us():
    """
    login cho trang user
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        next_url = request.args.get('next')
        if user and user.active == models.EStatus.Active and user.user_role_id != models.EUserRole.anonymous:
            flash("Login Success", category='success')
            login_user(user=user)
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index_user'))

        logout_user()
        if user:
            flash("Invalid username or password", category='error')
            user = None
    return render_template('login.html', form=form, title="Login User", action="login_us")


@app.route("/admin/login", methods=["GET", "POST"])
def login_admin():
    """
    login cho trang admin
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        next_url = request.args.get('next')

        if user and user.active == models.EStatus.Active and user.user_role_id == models.EUserRole.admin.value:
            login_user(user=user)

            flash("Login Success", category='success')
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index_admin'))

        logout_user()
        if user:
            flash("Invalid username or password", category='error')
            user = None

    return render_template('login.html', form=form, title='Login Admin', action='login_admin')


@app.route("/user/profile")
@app.route("/admin/profile")
@login_required
def profile():
    # request.args.get('id')
    # http: // 127.0.0.1: 5000 / admin / profile?id = 3f7d454b - 0283 - 4389 - a439 - b5e0b3a4c650
    """
    hiển thị thong tin chi tiết của user
    :return:
    """

    params = {
        'title': "Profile",
        'nav_user': 'active',

    }
    if current_user.user_role.id == models.EUserRole.admin.value:
        params['user'] = models.User.query.filter(models.User.user_name == "user").first()
        return render_template('profile.html', params=params)

    params['user'] = current_user
    return render_template('profile.html', params=params)


@app.route("/user/bloglist")
@app.route("/admin/bloglist")
@login_required
def blog_list():
    """
    admin: hiển thị tất cả bài viết của user
    user: hiển bài viết của user đó
    :return:
    """

    listblog = models.QL_BaiViet.query.all()

    params = {
        'title': "Blog List",
        'nav_blog': 'active',
        'listblog': listblog
    }

    if current_user.user_role.id == models.EUserRole.admin.value:

        return render_template('bloglist.html', params=params)
    return render_template('bloglist.html', params=params)




@app.route("/user/blog")
@app.route("/admin/blog")
def blog_detail():
    """
    hiển thị detail blog
    dùng template admin (blog.html)
    :return:
    """
    params = {
        'title': "title bài viết",
        'nav_blog': 'active',

    }
    if current_user.user_role.id == models.EUserRole.admin.value:
        return render_template('blogdetail.html', params=params)
    return render_template('blogdetail.html', params=params)




@app.route('/admin')
@login_required_Admin
def index_admin():
    """
    hiển thị biểu đồ or bài viết
    :return:
    """
    params = {
        'title': "Dashboard",
        'nav_dashboard': 'active',

    }

    return render_template('admin/index.html', params=params)


@app.route('/admin/userlist')
@login_required_Admin
def user_list():
    """
    hiển thị tất cả user trừ tài khoản admin hiện tại
    :return:
    """
    params = {
        'title': "User List",
        'nav_profile': 'active',

    }
    # test lấy dữ liệu
    listuser = models.User.query.all()
    params['listuser'] = listuser
    return render_template('admin/UserList.html', params=params)


@app.route('/user')
@login_required
def index_user():
    """
    hiển thị list bài viết của user đây
    :return:
    """
    # paramenter chứa danh sách tham số truyền ra template
    params = {
        'title': 'Dashboard',
        'nav_dashboard': 'active',
    }

    return render_template('user/index.html', params=params)


@app.route('/changepw', methods=["POST", "GET"])
@login_required
def change_password():
    """
    thay đổi password
    chưa làm : mã hóa mật khẩu
    :return:
    """
    params = {
        'title': "Change password",
        'nav_blog': 'active',

    }

    form = FormChange.FormChangePassword()
    if form.validate_on_submit():
        user = form.get_user()
        if user:
            user.password = generate_password_hash(form.password_Comfirm.data)
            print(user.user_name, user.password)
            db.Session.add(user)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('ChangePassword.html', form=form)


@app.route('/user/delete/blog', methods=["POST"])
@app.route('/admin/delete/blog', methods=["POST"])
@login_required
def delete_blog():
    """
    user: delete blog user đó
    admin: delete all blog
    nhận id bài viết
    gửi lên dạng post form có csrf
    :return: trang bloglist dùng redirect()
    """

    pass


@app.route('/admin/delete/user', methods=["POST"])
@login_required_Admin
def delete_user():
    """
    xóa user bằng cách cho trường active của user đó  = False or user.active = models.EStatus.InActive
    gửi yêu cầu dạng form có csrf

    :return: userlist dùng  redirect()
    """
    pass


# ================== làm cho anonymous ========================================


@app.route("/")
def index():
    """
    hiểm thị list các blog xắp xếp theo time giảm dần
    :return:
    """

    params = {
        'title': "Home",

    }
    bv = models.QL_BaiViet.query.all()
    params['QL_BaiViet'] = bv
    return render_template("home/index.html", params=params)


@app.route('/blog')
def blog():
    """
        blog detail
        kế thừa page.html tạo trang mới để hiển thị nội dung blog
    :return:
    """

    t = models.QL_BaiViet.title

    params = {
        'title': t,
        'nav-bd': 'active'
    }

    return render_template('profile.html', params=params)


@app.route("/aboutus")
def about_us():
    """
    còn time thì làm hiển thị thông tin của nhóm mình ở đây
    :return:
    """

    params = {
        'title': "Home",
        'nav_about': 'active'

    }

    return render_template('home/aboutus.html', params=params)


@app.route("/contact")
def contact():
    """
    làm không làm cũng đc
    :return:
    """
    params = {
        'title': "Home",
        'nav_contact': 'active'
    }

    return render_template('home/contact.html', params=params)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', code=404, ms='Error Page'), 404


@app.errorhandler(500)
def special_exception_handler(error):
    return render_template('error.html', code=500, ms='connection failed'.capitalize()), 500


if __name__ == "__main__":
    # app.run(debug=True,host="192.168.1.7",port="5000")
    app.run(debug=True)
