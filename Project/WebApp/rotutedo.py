from WebApp import app,login
from flask import render_template
from flask_login import login_required
from WebApp.Utils.changepassword import changepass, changeAccountInformation
from WebApp.Forms.FormChange import ChangePasswordForm,ChangeAccountInformationForm

@app.route("/changepass",methods=["GET","POST"])
@login_required
def ChangePass():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        return changepass(form)
    return render_template("changepassword.html",form=form)

@app.route("/changeaccount",methods=["GET","POST"])
@login_required
def change_Account_Information():
    form = ChangeAccountInformationForm()
    if form.validate_on_submit():
        return changeAccountInformation(form)
    return render_template("changeAccountInformation.html", form=form)
