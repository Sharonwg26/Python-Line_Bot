from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('OQqOlMprRqeiXhBHSymZ45X+i7WF74swYPh3nYpgcrVezoVQQ726Eqh2e0oBORceRt+brhEoSIC6W61E4H3bxGOg4Wp51V/XsG4QW4fIkPNrb/leolZ31igBf2WZd0cTnKS86EFUUWQy2TZNgHu6ugdB04t89/1O/w1cDnyilFU=
')
# Channel Secret
handler = WebhookHandler('69a5b0ff850e58d346a7695507d98177')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text='Hello, world')
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
