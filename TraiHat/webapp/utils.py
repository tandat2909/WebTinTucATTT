import hashlib
import datetime
import base64
import datetime
import os
import random
import re

import uuid

from webapp.config import Config
from webapp import models


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
        rac = str(os.urandom(20).hex())  # tạo chuỗi gây nhiễu
        a = random.randint(4, len(rac) - 8)  # random vị trí cắt chuỗi gây nhiễu
        rac = rac[a: a + random.randint(4, 8)]  # cắt lấy 4 ký tự gây nhiễu
        blocks = temp.split('-')  # cắt chuỗi theo lý tự '-'
        vt = random.randint(1, len(blocks) - 1)  # random vị trí thêm rac
        blocks.insert(vt, rac)  # thêm chuỗi gây nhiễu
        temp = "-".join(blocks)  # nối lại chuỗi vừa cắt
        temp = str(vt) + temp  # thêm vị trí của chuỗi gây nhiễu vào chuỗi vừa nối
        temp = temp[::-1].upper()  # đảo ngược chuỗi và in hoa các ký tự thường

        # mã hóa đoạn chuỗi trên bằng thuật toán base64
        output = base64.urlsafe_b64encode((temp).encode('utf-8')).decode("utf-8").replace('=','')
        output = output[::-1]  # đảo ngược chuỗi mã hóa
        output += rac[:4].upper()  # thêm 4 ký tự gây nhiễu vào cuối chuỗi mã hóa

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


if __name__ == '__main__':
    for i in range(100):
        data = 's-s'
        en = encodeID(data)
        de = decodeID(en)
        print("encode:", en, len(data))
        print("decode:", de, len(de))
