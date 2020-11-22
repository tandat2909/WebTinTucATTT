
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


def check_password(pw_hash='',pw_check=''):
    pw_check_hash = hashlib.sha256(pw_check.encode("utf-8")).hexdigest()
    if pw_hash == pw_check_hash:
        return True
    return False
def generate_password(pw):
    pw_hash = hashlib.sha256((pw+Config.KEYPASS).encode('utf-8')).hexdigest()
    return pw_hash
def encodeID(id = ""):
    try:
        rac =generate_password(str(datetime.datetime.now()))
        a = random.randint(0, len(rac) - 4)
        rac = rac[a: a +4] + "-"
        b = [m.start() for m in re.finditer("-", id)]
        vt = random.randint(0, len(b)-1)
        id1 = id[:b[vt]+1]
        id = id[b[vt]+1:]
        id = str(b[vt]) + "-5" + id1 + rac + id
        return base64.b64encode((id +Config.SECRET_KEY) .encode('utf-8')).decode("utf-8")
    except:
        return 'Error encode'
def decodeID(id):
    try:
        id = base64.b64decode(id).decode('utf-8')
        vt = int(id[: id.find("-")])
        lengh = int(id[id.find("-")+ 1: id.find("-")+ 2])
        id = id[id.find("-")+ 2 : ]
        result = id.replace(id[vt:vt+lengh],'',1).replace(Config.SECRET_KEY,'',1)
        return result
    except:
        return "ID truyền vào bằng rỗng"

if __name__ == '__main__':
    print(encodeID("ưqhiebquiyweghuihnq"))
    print(decodeID(encodeID("ưqhiebquiyweghuihnq")))

    print(generate_password("admin@123"))