
class thamso:
    server = 'TANDAT_2909\DBSQL2019_01'
    database = 'DBTinTuc'
    username = 'sa'
    password = 'root'
    driver = 'ODBC+Driver+17+for+SQL+Server'
class Config(object):
    SQLALCHEMY_DATABASE_URI=str.format(f"mssql+pyodbc://{thamso.username}:{thamso.password}@{thamso.server}/{thamso.database}?driver={thamso.driver}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = b'=xx08_xe2xd6o#$%x0cxadxad'
    FLASK_APP = "WEBTinTuc"



if __name__ == "__main__":
    print(Config.SQLALCHEMY_DATABASE_URI)
    for v in Config.SECRET_KEY:
        print(v)