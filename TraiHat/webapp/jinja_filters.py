from webapp import utils
from webapp import app


def encodeID(value):
    try:
        en = utils.encodeID(value)
        return en
    except:
        return ''

app.jinja_env.filters['encodeID'] = utils.encodeID
