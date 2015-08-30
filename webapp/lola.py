import hashlib
from flask import Flask, request

application = Flask(__name__)


@application.route('/')
def hello():
    return "<h1>The Ballad of Jo & Lo</h1>"


@application.route('/about')
def about():
    return "<h1>by Joshua G</h1>"


@application.route('/wechat')
def wechat_auth():
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']

    token = 'lola'

    a = [token, timestamp, nonce]
    a.sort()

    m = hashlib.sha1()
    m.update(a[0] + a[1] + a[2])

    if m.hexdigest() == signature:
        return request.args['echostr']
    else:
        return 'N/A'


if __name__ == "__main__":
    application.run(host='0.0.0.0')
