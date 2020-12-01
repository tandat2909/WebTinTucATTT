class thamso:
    server = 'TANDAT_2909\DBSQL2019_01'
    database = 'DBTinTuc'
    username = 'sa'
    password = 'root'
    driver = 'ODBC+Driver+17+for+SQL+Server'
class Config(object):
    SQLALCHEMY_DATABASE_URI=str.format(f"mssql+pyodbc://{thamso.username}:{thamso.password}@{thamso.server}/{thamso.database}?driver={thamso.driver}")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '=xx08_xe2xd6o#$%x0cxadxad'
    KEYPASS = '@blog'

    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    WTF_CSRF_TIME_LIMIT = 3600
    WTF_CSRF_ENABLED = True
   # FLASK_ADMIN_SWATCH="swatch"
    FLASK_ADMIN_FLUID_LAYOUT = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    SESSION_COOKIE_AGE = 1  # set just 10 seconds to test
    SESSION_SAVE_EVERY_REQUEST = True


if __name__ == "__main__":
    print(Config.SQLALCHEMY_DATABASE_URI)
    for v in Config.SECRET_KEY:
        print(v)