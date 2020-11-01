from WebApp import app, db, login
import uuid
from sqlalchemy import Column, Integer, String, Float, ForeignKey,BigInteger,Boolean
import datetime
from WebApp.DataModels.Enums import Enum_Gender,Enum_Status_Account

class Account(db.Model):
    __tablename__= "Account"
    account_ID = Column(String(200),primary_key=True,default=uuid.uuid1())
    user_Name = Column(String,nullable=False)
    password_Hash = Column(String, nullable= False)
    role = Column(String)
    regiter_Date = Column(String,nullable=False,default= str(datetime.datetime.now()))
    status = Column(Boolean,nullable=False,default=Enum_Status_Account["Active"])
    full_Name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone_Number = Column(String(20), nullable=True)
    # bút danh
    pseudonym = Column(String)
    gender = Column(String, default=Enum_Gender[0])

    # relationship

     #posts = db.relationship('Post', backref='author', lazy='dynamic')

    #end relationship


    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
       return str(self.account_ID)  # python 3

    def __repr__(self):
        return '<Account AccountID = {} ,user_Name = {}>'.format(self.account_ID, self.full_Name)


@login.user_loader
def load_user(id):
    return Account.query.get(str(id))







if __name__ =="__main__":
    db.create_all()

