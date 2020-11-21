from datetime import datetime, date
from Team1 import app, db
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
import pyodbc



class Loai_User(db.Model):
    __tablename__ = "Loai_User"
    loaiID = Column(String(3), primary_key=True)
    tenLoai = Column(String(20), nullable=False)
    user = relationship('QL_User', backref='author', lazy='dynamic')



class QL_LoaiBT(db.Model):
    __tablename__ = "QL_LoaiBT"
    loaiBT = Column(String(10), primary_key=True, nullable=False)
    tenLoaiBT = Column(String(20), nullable=False)
    chuDe = relationship('QL_BaiViet', backref='chude', lazy='dynamic')


class QL_User(db.Model):
    __tablename__ = "QL_User"
    UserID = Column(String(50), primary_key=True)
    userName = Column(String(30), nullable=False)
    Pw = Column(String(20), nullable=False)
    hoTen = Column(String(100), nullable=False)
    gioiTinh = Column(String(10), nullable=False)
    ngaySinh = Column(String)
    ngayTao = Column(String)
    loaiID = Column(String(3), ForeignKey(Loai_User.loaiID), nullable=False)
    email = Column(String(100), nullable=False)
    sdt = Column(String(10), nullable=False)
    user_bv = relationship('QL_BaiViet', backref='userid', lazy=True)



class QL_BaiViet(db.Model):
    __tablename__ = "QL_BaiViet"
    baiVietID = Column(String(10), primary_key=True)
    userID = Column(String(50), ForeignKey(QL_User.UserID), nullable=False)
    noiDung = Column(String(1000))
    chuDe = Column(String(10), ForeignKey(QL_LoaiBT.loaiBT), nullable=False)
    ngayDangTin = Column(String)
    pheDuyet = Column(Integer)


if __name__ == '__main__':
    db.create_all()
    ngSinh = "23 October, 2000"
    now = datetime.now()
    loaiUser =Loai_User(loaiID='u3',tenLoai='huygf')
    loaiBt = QL_LoaiBT(loaiBT='tw', tenLoaiBT='Am nhac')
    user = QL_User(UserID = 'user4', userName='lan', Pw='123', hoTen='Nguyen Lan', gioiTinh='nu',
                   ngaySinh='23/10/2000',ngayTao=now.strftime('%m/%d/%Y') , author=loaiUser, email='1234', sdt='034788765')
    baiViet = QL_BaiViet(baiVietID='baiviet4', userid=user, noiDung='ngay mai',
                         chude=loaiBt, ngayDangTin=now.strftime('%m/%d/%Y'), pheDuyet=0)
    db.session.add(loaiUser)
    db.session.add(loaiBt)
    db.session.add(user)
    db.session.add(baiViet)
    db.session.commit()

    for i in Loai_User.query.all():
        print(i.loaiID)



