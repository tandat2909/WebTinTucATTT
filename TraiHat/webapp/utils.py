import hashlib
import datetime
import base64
import datetime
import json
import os
import random
import re

import uuid
from webapp import models

from webapp.config import Config
from webapp import models, db


def check_password(pw_hash='', pw_check=''):
    pw_check_hash = hashlib.sha256(pw_check.encode("utf-8")).hexdigest()

    if pw_hash == pw_check_hash:
        return True
    return False


def generate_password(pw):
    pw_hash = hashlib.sha256((pw + Config.KEYPASS).encode('utf-8')).hexdigest()
    return pw_hash


def encodeID(input="-"):
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
    temp = str(input)
    result = ''
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
    print(get_blog_by_ID(decodeID('ETOBFDOwATO30CM1YTRGNTLCBzQ10CNBNUMtgDOzITL4MUQyIUM1UDOwEUN056E')).title)
    print(decodeID('0kTQxgDMwkzNtIEMDVTL0E0Qx0CO4MjMtcTREF0QykTL4MUQyIUM1UDOwEUN7EDA'))
    img = '{"0":"sdf","1":"sdf"}'
    ids = json.loads(img)
    print(ids)
    os.mkdir('static/image/blog/sd')
    print(img)
