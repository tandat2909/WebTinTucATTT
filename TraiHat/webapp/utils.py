import hashlib
import datetime
import base64
import datetime
import os
import random
import re

import uuid

from webapp.config import Config
from webapp.models import User


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
    temp = input
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
        output = base64.urlsafe_b64encode((temp).encode('utf-8')).decode("utf-8").replace('=','')
        # đảo ngược chuỗi mã hóa
        output = output[::-1]
        # thêm 4 ký tự gây nhiễu vào cuối chuỗi mã hóa
        output += rac[:4].upper()

        return output

    except:
        return 'Error encode'


def decodeID(input):
    temp = input
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

    except:
        return "Decode Error"

def get_user_id(user_id):

    user_id = decodeID(user_id)

    return User.query.get(user_id)


if __name__ == '__main__':
    for i in range(100):
        data = 's-s'
        en = encodeID(data)
        de = decodeID(en)
        print("encode:", en, len(data))
        print("decode:", de, len(de))
