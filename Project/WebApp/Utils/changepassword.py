from WebApp.DataModels.AccountModels import Account
from flask_login import current_user
from WebApp.Forms.FormChange import ChangePasswordForm,ChangeAccountInformationForm
from WebApp import db
def changepass(formchangepass):
    try:
        if current_user.password_Hash == formchangepass.password_Old.data:

            if formchangepass.password_Comfirm.data == formchangepass.password_New.data:

                current_user.password_Hash = formchangepass.password_New.data
                return "Đổi pass thành công"
            else:
                return "Pass không đúng"
        return "pass cũ sai nhập lại"
    except:
        return "bạn tuổi lol đổi đc nhá "

def changeAccountInformation(form):
    try:
        if form.password.data == current_user.password_Hash:
            current_user.user_Name = form.userName_New.data
            current_user.full_Name = form.fullName_New.data
            current_user.email = form.email_New.data
            current_user.phone_Number = form.phoneNumber_New.data
            current_user.pseudonym = form.pseudonym_New.data
            current_user.gender = form.gender_New.data
        else:
            return "Nhập sai mật khẩu!"
    except:
        return "bạn tuổi lol đổi đc nhá "




