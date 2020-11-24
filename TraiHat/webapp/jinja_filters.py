import os

from webapp import utils
from webapp import app
import uuid

def encodeID(value):
    try:
        en = utils.encodeID(value)
        return en
    except:
        return ''
def insert_id_form(value):
    try:
        formid = os.urandom(10).hex() + '-' + str(value)
        if utils.add_form_id(formid):
            return encodeID(formid)
        raise
    except Exception as ev:
        return ''


app.jinja_env.filters['encodeID'] = encodeID
app.jinja_env.filters['insert_id_form'] =insert_id_form
