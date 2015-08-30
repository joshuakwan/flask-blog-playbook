import hashlib
from flask import Flask, request
from wechat_sdk import WechatBasic

application = Flask(__name__)

token = 'lola'
wechat_processor = WechatBasic(token=token)


@application.route('/', methods=['GET', 'POST'])
def hello():
    return "<h1>The Ballad of Jo & Lo</h1>"


@application.route('/about')
def about():
    return "<h1>by Joshua G</h1>"


@application.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        return wechat_auth(request)
    if request.method == 'POST':
        if wechat_processor.check_signature(signature=request.args['signature'], timestamp=request.args['timestamp'],
                                            nonce=request.args['nonce']):
            wechat_processor.parse_data(request.data)
            message = wechat_processor.get_message()

            response = None
            if message.type == 'text':
                if message.content == 'who are you?':
                    response = wechat_processor.response_text(u'I am bot Lola')
                else:
                    response = wechat_processor.response_text(u'You send me a text')
            elif message.type == 'image':
                response = wechat_processor.response_text(u'You send me an image')
            else:
                response = wechat_processor.response_text(u'unknown')

            return response


def wechat_auth(wechat_request):
    signature = wechat_request.args['signature']
    timestamp = wechat_request.args['timestamp']
    nonce = wechat_request.args['nonce']

    a = [token, timestamp, nonce]
    a.sort()

    m = hashlib.sha1()
    m.update(a[0] + a[1] + a[2])

    if m.hexdigest() == signature:
        return wechat_request.args['echostr']
    else:
        return 'N/A'


if __name__ == "__main__":
    application.run(host='0.0.0.0')
