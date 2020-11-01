from WebApp import app,db
from flask_admin import Admin, AdminIndexView, expose


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

admin = Admin(app, name="Admin Quản Lý Web Site")
