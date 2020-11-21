server = 'DESKTOP-98TOBJM'
database = 'DBTinTuc'
username = 'SqlLogin1'
password = '12'
driver = 'ODBC+Driver+17+for+SQL+Server'

class Config(object):
    SQLALCHEMY_DATABASE_URI=str.format(f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = b'=xx08_xe2xd6o#$%x0cxadxad'

