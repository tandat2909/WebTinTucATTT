
import hashlib
import datetime
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



if __name__ == '__main__':

    print(generate_password("admin@123"))