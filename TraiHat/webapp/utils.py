import hashlib, datetime, base64, os, random, re, uuid
from sqlalchemy import or_
from webapp.config import Config
from webapp import models, db
import yagmail,json


def check_password(pw_hash='', pw_check=''):
    pw_check_hash = hashlib.sha256(pw_check.encode("utf-8")).hexdigest()

    if pw_hash == pw_check_hash:
        return True
    return False


def generate_password(pw):
    pw_hash = hashlib.sha256((pw + Config.KEYPASS).encode('utf-8')).hexdigest()
    return pw_hash


def encodeID(input="-"):
    """

    :param input:
    :return:
    :exception Exception
    """

    # print("input:",input)
    temp = str(input)
    output = ""
    try:
        # tạo chuỗi gây nhiễu
        rac = str(os.urandom(20).hex())
        # random vị trí cắt chuỗi gây nhiễu
        a = random.randint(4, len(rac) - 8)
        # cắt lấy 4 ký tự gây nhiễu
        rac = rac[a: a + random.randint(4, 8)]
        # cắt chuỗi theo lý tự '-'
        blocks = temp.split('-')
        # random vị trí thêm rac
        vt = random.randint(1, len(blocks) - 1)
        # thêm chuỗi gây nhiễu
        blocks.insert(vt, rac)
        # nối lại chuỗi vừa cắt
        temp = "-".join(blocks)
        # thêm vị trí của chuỗi gây nhiễu vào chuỗi vừa nối
        temp = str(vt) + temp
        # đảo ngược chuỗi và in hoa các ký tự thường
        temp = temp[::-1].upper()
        # mã hóa đoạn chuỗi trên bằng thuật toán base64
        output = base64.urlsafe_b64encode((temp).encode('utf-8')).decode("utf-8").replace('=', '')
        # đảo ngược chuỗi mã hóa
        output = output[::-1]
        # thêm 4 ký tự gây nhiễu vào cuối chuỗi mã hóa
        output += rac[:4].upper()

        return output

    except Exception as ex:
        raise ex


def decodeID(input):
    """

    :param input:
    :return:
    :exception Exception
    """
    temp = str(input)
    try:
        temp = temp[:-4]
        temp = temp[::-1]
        decode_temp = ''

        for i in range(3):
            try:
                decode_temp = base64.urlsafe_b64decode(temp).decode('utf-8').lower()
                break
            except:
                temp += '='
                continue

        decode_temp = decode_temp[::-1]
        vt_block = int(decode_temp[:1])
        decode_temp = decode_temp[1:]
        blocks = decode_temp.split('-')
        blocks.pop(vt_block)
        result = '-'.join(blocks)

        return result

    except Exception as ex:
        raise ex


def check_form_register(form):
    """
     kiểm tra đầu vào form
    :param form:
    :return:
    :exception ValueError
    """
    if form:
        # validate password
        if form.password.data != form.confirm.data:
            raise ValueError("Incorrect confirm password")
        user = models.User.query.filter(
            or_(models.User.user_name == form.username.data, models.User.email == form.email.data)).first()

        # validate email, user
        if user:
            if user.user_name == form.username.data:
                raise ValueError("Invalid Username")
            if user.email == form.email.data:
                raise ValueError("Invalid Email")
        return True
    raise ValueError("Error Form")


def save_user(form, confirm: bool):
    """
    :param confirm:
    :param form: type dict()
    :return: Return True if it commit to database success else False which commit or password hashing failde
    """

    try:
        if form:
            password = generate_password(form.get('password', None))
            usernew = models.User(user_name=form.get('username', None),
                                  password=password,
                                  email=form.get('email', None),
                                  pseudonym=form.get('pseudonym', None),
                                  user_role_id=models.EUserRole.editor.value,
                                  name=' '.join([form.get('firstname', None), form.get('lastname', None)]),
                                  firstname=form.get('firstname', None),
                                  lastname=form.get('lastname', None),
                                  gender=form.get('gender', None),
                                  address=form.get('address', None),
                                  phone_number=form.get('phone_number', None),
                                  confirm=confirm
                                  )
            db.session.add(usernew)
            db.session.commit()
            return True
        return False
    except:
        return False


def sent_mail_confirm_code(email: str, code: str):
    """
    gửi mã xác nhận
    :param email:
    :param code:
    :return:
    """
    if email and code:
        sender_email = "antoanhethongthongtin13@gmail.com"
        receiver_email = email
        password = decodeID("ETUXVUUXVUMyMDQtgjRwMEMClTL8F0C")[0:-1].capitalize()
        subject = "Bloger"
        body = f"Confirm Account \n Code: {code}"

        yag = yagmail.SMTP(user=sender_email, password=password)
        status = yag.send(
            to=receiver_email,
            subject=subject,
            contents=body,

        )
        return False if status == False else True
    return False


def generate_codeConfirm():
    """
    tạo mã xác nhận
    :return:
    """
    temp = str(uuid.uuid4().hex)[:6]
    return temp


def check_timeout(date: str):
    """
    kiểm tra timeout
    :param date:
    :return:
    """
    if date:
        # 10 phút
        timeout = 600
        current_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        timedelta = (datetime.datetime.now() - current_time).total_seconds()
        # print(timedelta)
        if 0 < timedelta < timeout:
            return True
    return False


def lock_account(current_user, user_id, lock: bool = None):
    try:
        if current_user.user_role_id == models.EUserRole.admin.value and user_id and lock is not None:
            if current_user.id != decodeID(user_id):
                user = models.User.query.get(decodeID(user_id))
                user.active = models.EStatus.InActive if lock else models.EStatus.Active
                db.session.add(user)
                db.session.commit()
                return True
        return False
    except:
        return False


def get_blog_by_userID(id: str):
    blogs = models.QL_BaiViet.query.filter(id == models.QL_BaiViet.user_id)
    return blogs


def get_blog_by_ID(id: str):
    print(id)
    blog = models.QL_BaiViet.query.get(decodeID(id))
    return blog


def save_blog(title, data, user, chude, imgs):
    try:
        if title and data and user and user.user_role_id != models.EUserRole.admin.value:

            post = models.QL_BaiViet(id=uuid.uuid4(), title=title, noiDung=data, user_id=user.id, chuDe_id=chude)
            if imgs:
                imgjson = json.loads(imgs)
                path = 'static/image/blog/' + str(post.id) + '/'
                os.mkdir(path)
                for k, v in imgjson.items():
                    img = v[v.find(",") + 1:]
                    with open(path + k + ".png", 'wb') as file_to_save:
                        decoded_image_data = base64.decodebytes(img.encode('utf-8'))
                        file_to_save.write(decoded_image_data)
                post.image = '/'+path
            db.session.add(post)
            db.session.commit()
            return True, str(post.id)
        return False, None
    except:
        return False, None


if __name__ == '__main__':
    print(check_timeout('2020-11-28 22:03:55.171404'))
    print(decodeID('gMxkDOENUQFVTL1MTM00CREN0QyMENC1CN3cjQtgzQxYULzIkQzYkQEFEN4QDODDCC'))
