import hashlib
import datetime
import base64
import datetime
import os
import random
import re

import uuid
from webapp import models

from webapp.config import Config
from webapp import models,listFormID


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
        output = base64.urlsafe_b64encode((temp).encode('utf-8')).decode("utf-8").replace('=','')
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

def get_blog_by_userID(id:str):
    blogs = models.QL_BaiViet.query.filter(id == models.QL_BaiViet.user_id)
    return blogs
def get_blog_by_ID(id:str):
    blog = models.QL_BaiViet.query.get(decodeID(id))
    return blog

def check_form_exist(formID:str):
    try:
        #print(listFormID.get('FormDelete'))
        listFormID.get('FormDelete').remove(decodeID(str(formID)))
       # print(listFormID.get('FormDelete'))
        return True
    except:
        return False
def add_form_id(formid):
    try:

        listFormID.get('FormDelete').append(str(formid))
        print(listFormID.get('FormDelete'))
        return True
    except:
        return ''

def deleteBlog(blogid,user):

    try:
        blog = models.QL_BaiViet.query.get(decodeID(blogid))
        if blog:
            if user.user_role_id == models.EUserRole.admin.value:

                return True
            elif user.id == blog.user_id:
                return True

            else:
                raise
        else:
           raise
    except:
        return False

if __name__ == '__main__':

   id = models.User.query.all()[0].id
   #print(encodeID(str(id)))
    #for i in range(100):
    #    data = 's-s'
    #    en = encodeID(data)
    #    de = decodeID(en)
    #    print("encode:", en, len(data))
    #    print("decode:", de, len(de))
#

    for i in range(6):
        add_form_id()
    print(listFormID.get("FormDelete"))
    for i in range(6):
        print(check_form_exist(encodeID(listFormID.get("FormDelete")[i])))
    print(listFormID.get("FormDelete"))
