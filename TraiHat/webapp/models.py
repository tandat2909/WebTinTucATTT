from webapp import app, db, login
import uuid, datetime
from sqlalchemy import Column, Enum as EnumSQL, Integer, NVARCHAR, DATETIME, Float, ForeignKey, BigInteger, Boolean, \
    Unicode, UnicodeText,NVARCHAR
# from webapp.Enums import Enum_Gender,Enum_Status_Account
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.orm import relationship, lazyload
from sqlalchemy_utils import UUIDType, ChoiceType, IPAddressType, PasswordType, Password
from enum import Enum


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(NVARCHAR)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id


class EUserRole(Enum):
    anonymous = 1
    content_writer = 2
    regular_user = 3

    editor = 4

    admin = 5


class UserRole(BaseModel):
    __tablename__ = "UserRole"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_userrole = relationship("User", backref="user_role", lazy=True)

class EStatus(Enum):
    Active = True
    InActive = False


class AnonymousUser(AnonymousUserMixin):
    user_id = uuid.uuid4
    user_name = "Anonymous"
    user_role_id = EUserRole.anonymous
    timelogin = datetime.datetime.now()

    def get_id(self):
        return self.user_id

    def __str__(self):
        return self.user_name


class User(BaseModel, UserMixin):
    __tablename__ = "User"

    user_name = Column(NVARCHAR, nullable=False)
    password = Column(NVARCHAR, nullable=False)
    lastname = Column(NVARCHAR)
    firstname = Column(NVARCHAR)
    # role = Column(NVARCHAR)
    regiter_date = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    address = Column(NVARCHAR)
    email = Column(NVARCHAR, nullable=True)
    phone_number = Column(NVARCHAR(20), nullable=True)
    avatar = Column(NVARCHAR)
    # bút danh
    pseudonym = Column(Unicode)
    gender = Column(Unicode, default="")
    confirm = Column(Boolean, nullable=False, default=False)

    # relationship

    posts = relationship('QL_BaiViet', backref='user', lazy=True)

    # end relationship

    # ForeignKey
    user_role_id = Column(Integer, ForeignKey(UserRole.id), nullable=False, default=EUserRole.anonymous)
    active = Column(EnumSQL(EStatus), nullable=False, default=EStatus.Active)

    # End ForeignKey



class QL_LoaiBT(BaseModel):
    __tablename__ = "QL_LoaiBT"
    id = Column(Integer,primary_key=True,autoincrement=True)
    chuDe_fk_QL_LoaiBT = relationship('QL_BaiViet', backref='chude', lazy=True)


class QL_BaiViet(BaseModel):
    __tablename__ = "QL_BaiViet"

    title = Column(NVARCHAR,nullable=False,default="")
    noiDung = Column(NVARCHAR)
    ngayDangTin = Column(DATETIME)
    ngaytaobaiviet = Column(DATETIME,nullable=False,default=datetime.datetime.now())
    pheDuyet = Column(Boolean,nullable=False,default=True)
    image = Column(NVARCHAR)
    chuDe_id = Column(Integer, ForeignKey(QL_LoaiBT.id), nullable=False)
    user_id = Column(UUIDType, ForeignKey(User.id), nullable=False)




@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def insertUserType():
    usrole1 = UserRole(name="Anonymous")
    usrole3 = UserRole(name="Regular User")
    usrole4 = UserRole(name="Editor")
    usrole2 = UserRole(name="Content Writer")
    usrole5 = UserRole(name="Admin")
    db.session.add(usrole1)
    db.session.add(usrole2)
    db.session.add(usrole3)
    db.session.add(usrole4)
    db.session.add(usrole5)


def insertUser():
    us1 = User(user_name='admin', address=u"3773, nguyễn kiệm gò vấp tphcm",
               password='d047de6de9348ed903f6ac3631731f26dc3795e09b07f6d3ac993d5f48045558',
               email='vutandat29092000@gmail.com',
               name=u'Tấn Đạt',
               confirm=True,
               user_role_id=EUserRole.admin.value,
               pseudonym="ADMIN"

    )
    us2 = User(user_name='user',
               password='d047de6de9348ed903f6ac3631731f26dc3795e09b07f6d3ac993d5f48045558',
               name='User',
               address=u"3773, nguyễn kiệm gò vấp tphcm",
               firstname="Tấn",
               lastname = "Đạt",
               confirm=True,
               user_role_id=EUserRole.editor.value,
               pseudonym = 'Giang pro',
               email='vutandat29092000@gmail.com')
    db.session.add(us1)
    db.session.add(us2)

def inserCategoryPost():
    cate1 = QL_LoaiBT(name="Tin Tức")
    cate2 = QL_LoaiBT(name="Thể Thao")
    cate3 = QL_LoaiBT(name = "Giải trí")
    db.session.add(cate1)
    db.session.add(cate2)
    db.session.add(cate3)
def inserPost(user1 ,user2):
    ps1 = QL_BaiViet(title="tào lao nhất quả đất",
                     noiDung="ờ thằng này tào lao thật",
                     user_id=user1.id,
                     chuDe_id=1,
                     image="admin2/images/img-1.jpg"
                      )
    ps2 = QL_BaiViet(title="Bitcoin tăng vọt, tiến sát 19.000 USD một đồng",
                     noiDung='Giá Bitcoin tăng 4% hôm qua (20/11) sau khi BlackRock nhận định tiền ảo này có thể thay thế vàng.'
                             'Tôi nghĩ rằng Bitcoin là một cơ chế bền vững có thể thay thế vàng trong phần lớn trường hợp, '
                             'vì nó có nhiều chức năng hơn là chuyền đi chuyền lại một thỏi vàng", Rick Rieder - Giám đốc Đầu '
                             'tư Tài sản trả lãi cố định tại BlackRock cho biết trên CNBC.'
                            'BlackRock hiện là công ty đầu tư hàng đầu thế giới, quản lý gần 8.000 tỷ USD tài sản. Sự ủng hộ của '
                             'BlackRock là dấu hiệu mới nhất cho thấy Bitcoin đang dần tiến vào ngành tài chính chính thống. Sau '
                             'bình luận của Rieder, giá Bitcoin lên tới 18.823 USD một đồng - tiến sát mức đỉnh gần 20.000 USD '
                             'thiết lập tháng 12/2017',
                     user_id=user2.id,
                     chuDe_id=3,
                     image="admin2/images/img-2.jpg"
                      )
    ps3 = QL_BaiViet(title="là dấu hiệu mới nhất cho thấy Bitcoin ",
                     noiDung="BlackRock hiện là công ty đầu tư hàng đầu thế giới, quản ",
                     user_id=user1.id,
                     chuDe_id=2,
                     image="không có ảnh"
                      )
    ps4 = QL_BaiViet(title="tthiết lập tháng 12/2017t",
                     noiDung="n của Rieder, giá Bitcoin lên tới 18",
                     user_id=user2.id,
                     chuDe_id=1,
                     image="không có ảnh"
                      )
    db.session.add(ps1)
    db.session.add(ps2)
    db.session.add(ps3)
    db.session.add(ps4)

if __name__ == "__main__":

    db.drop_all()
    db.create_all()
    insertUserType()
    insertUser()
    inserCategoryPost()
    use = User.query.all()
    inserPost(use[0],use[1])

    db.session.commit()
