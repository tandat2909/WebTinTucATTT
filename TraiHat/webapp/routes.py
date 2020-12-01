import datetime
from functools import wraps
import hashlib,uuid
from flask import url_for, request, redirect, render_template, session, abort, Response, g, flash, current_app, jsonify
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_login import login_user, login_required
from markupsafe import Markup
from wtforms import validators, PasswordField, HiddenField, StringField, Field, widgets, ValidationError
from wtforms.compat import text_type
from wtforms.widgets.core import Input
from webapp import app, db, models, login,jinja_filters,utils
from flask_login import login_user, current_user, logout_user, AnonymousUserMixin
from webapp.models import User
# from webapp.admin.routeAdmin import *
from webapp.Forms.FormLogin import LoginForm
from webapp.Forms.FormRegister import RegisterForm
from webapp.Forms import FormChange, FormRegister
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


def login_required_editor(f):
    """
    bắt buộc đăng nhập với quyền editor
    :param f: function
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or not current_user.is_authenticated or current_user.user_role_id != models.EUserRole.editor.value:
            flash('Please login to access this page.')
            return redirect(url_for('login_us', next=request.url_rule))
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
        if user and user.active == models.EStatus.Active and user.confirm and user.user_role_id != models.EUserRole.anonymous:
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

        if user and user.active == models.EStatus.Active and user.confirm and user.user_role_id == models.EUserRole.admin.value:
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
    id_user = request.args.get("id")
    # print(id_blog)
    if id_user is None:
        abort(404)
    params = {
        'title': "Profile",
        'nav_user': 'active'
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
    params = {
        'title': "Blog List",
        'nav_blog': 'active',

    }

    if current_user.user_role.id == models.EUserRole.admin.value:
        params['listblog'] = models.QL_BaiViet.query.all()
        return render_template('bloglist.html', params=params)
    params['listblog'] = utils.get_blog_by_userID(current_user.id)
    return render_template('bloglist.html', params=params)




@app.route("/user/blogdetail")
@app.route("/admin/blogdetail")
def blog_detail():
    """
    hiển thị detail blog
    dùng template admin (blog.html)
    :return:
    """
    id_blog = request.args.get("id")
    #print(id_blog)
    if id_blog is None:
        abort(404)
    params = {
        'title': "title bài viết",
        'nav_blog': 'active',
        'blog': utils.get_blog_by_ID(id_blog)
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

    listuser = models.User.query.filter(models.User.id != current_user.id)
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

    if current_user.user_role.id == models.EUserRole.admin.value:
        params['listblog'] = models.QL_BaiViet.query.all()
        return render_template('bloglist.html', params=params)
    params['listblog'] = utils.get_blog_by_userID(current_user.id)
    return render_template('bloglist.html', params=params)


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
            user.password = generate_password_hash(form.password_Confirm.data)
            print(user.user_name, user.password)
            db.Session.add(user)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('ChangePassword.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    logout_user()
    """
    đăng ký tài khoản cho user
    :return:
    """
    params = {
        'title': 'Register',
    }

    form = RegisterForm()
    if session and session.get('register_form', None) is None:
        session['register_form'] = {}
    if form.validate_on_submit():
        try:
            if utils.check_form_register(form):
                idf = str(uuid.uuid4()).lower()
                session['register_form'][idf] = {}
                data_form_in_session = session['register_form'][idf]
                data_form_in_session['form'] = form.get_dict()
                code = utils.generate_codeConfirm()
                data_form_in_session['code_confirm'] = code
                utils.sent_mail_confirm_code(form.email.data, code)
                data_form_in_session['current_time'] = str(datetime.datetime.now())
                session['register_form'][idf] = data_form_in_session
                params['email'] = form.email.data
                params['idf'] = utils.encodeID(idf)
                params['title'] = "Confirm Email"
                return render_template('confirmCode.html', params=params)

        except ValueError as e:
            flash(str(e), category='error')
        except Exception as e:
            print('register error:' + e)
            # flash('looi router regitser: ' + str(e))

    params['form'] = form
    return render_template('register.html', params=params)


@app.route('/register/confirm', methods=["POST", "GET"])
def confirm_account():
    idf = None
    # kiểm tra id và time của form còn tồn tại hay không
    try:
        # print('session commit', session.items())
        idf = utils.decodeID(request.args.get('idf', None))
        time = session['register_form'][idf]['current_time']
        if not utils.check_timeout(time):
            raise TimeoutError('Code timeout đăng ký lại')

    except TimeoutError as ex:
        session['register_form'].pop(idf)
        abort(404)
    except:
        abort(404)

    # method POST
    if request.method == "POST":
        try:
            code = request.form.get('confemail', None)
            data_form = session['register_form'].get(idf, None)

            if data_form and code:
                if code == data_form.get('code_confirm'):
                    if utils.save_user(data_form.get('form'), confirm=True):
                        session['register_form'].pop(idf)
                        flash("Confirm Email Success", category='success')
                        return redirect(url_for('login_us'))

                raise KeyError('Code Confirm Invalid')

            raise TimeoutError('Code timeout đăng ký lại')

        except KeyError as ex:
            flash(ex)
        except TimeoutError as ex:
            session['register_form'].pop(idf)
            abort(404)
        except:
            abort(404)

    # method GET
    params = {'title': 'Confirm Email', 'email': session['register_form'][idf]['form'].get('email')}
    return render_template('confirmCode.html', params=params)


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
    if request.method == "POST":
        idF = request.form.get('ids ')
        if idF:
            flash(request.form.get(idF))
        else:
            flash("Lõi chét dủi mẹ",category='error')
    return redirect(url_for('blog_list'))



@app.route('/admin/lock/user', methods=["POST"])
@login_required_Admin
def lock_user():
    """
    xóa user bằng cách cho trường active của user đó  = False or user.active = models.EStatus.InActive
    gửi yêu cầu dạng form có csrf

    :return: trả về thông báo xóa thành công hay không

    """

    try:
        if current_user.user_role.id == models.EUserRole.admin.value:
            data = request.json
            lock = data.get('lock')
            user_id = data.get("idu")
            #print(user_id, lock)
            if lock == 'lock':
                if utils.lock_account(current_user=current_user, user_id=user_id, lock=True):
                    return jsonify({
                        "status": 200,
                        "data": "unlock"
                    })
            if lock == 'unlock':
                if utils.lock_account(current_user=current_user, user_id=user_id, lock=False):
                    return jsonify({
                        "status": 200,
                        "data": "lock"
                    })
        raise
    except:
        return jsonify({
            "status": 404,
            "data": "Error"
        })


# ================== làm cho anonymous ========================================


@app.route("/")
def index():
    """
    hiểm thị list các blog xắp xếp theo time giảm dần
    :return:
    """

    params = {
        'title': "Home",
        'blog': models.QL_BaiViet.query.all()

    }

    return render_template("home/index.html", params=params)


@app.route('/blog')
def blog():
    id_blog = request.args.get("id")
    if id_blog is None:
        abort(404)
    params = {'title': "Home",
            'blogs' : models.QL_BaiViet.query.all(),
            'blog': utils.get_blog_by_ID(id_blog)
    }

    return render_template("home/blogdetail.html", params=params)


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

@app.route("/user/addblog",methods=["POST", "GET"])
@login_required
def addblog():

    params = {
        'title': "Add Blog",
        'nav_contact': 'active'
    }
    if request.method == "POST":
        data = request.form.get('datablog')
        imgs = request.form.get('imageblog')
        #print("addblog",imgs)
        title = request.form.get('titleblog')
        status, idblog = utils.save_blog(title=title,data=data,user=current_user,chude=1,imgs = imgs)
        #print(status,idblog)
        if status:
            flash("Add Blog Success")
            return redirect("/user/blogdetail?id=" + utils.encodeID(idblog))
    return render_template('user/addblog.html', params=params)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', code=404, ms='Error Page'), 404


@app.errorhandler(500)
def special_exception_handler(error):
    return render_template('error.html', code=500, ms='connection failed'.capitalize()), 500


if __name__ == "__main__":
    app.run(debug=True)
