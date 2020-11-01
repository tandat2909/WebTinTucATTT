from WebApp import app, db
from flask import render_template, redirect, request, url_for, flash

from flask_login import login_user, login_required, logout_user, current_user

from sqlalchemy import func
from WebApp.DataModels.AccountModels import Account

from WebApp.Forms.FormLogin import LoginForm


@app.route('/')
@app.route('/Home')
def Home():
    return render_template("Home.html",current_user= current_user)


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = Account.query.filter(Account.user_Name == username, Account.password_Hash == password).first()
        if user:
            login_user(user=user)

    return redirect("/admin")



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter(Account.user_Name == form.username.data, Account.password_Hash == form.password.data).first()
        print(user)
        if user:
            login_user(user=user)
        return redirect('Home')
    return render_template('login/login.html', title='Sign In', form=form)


if __name__ == '__main__':
    # print(app.secret_key)
    app.run(debug=True)
