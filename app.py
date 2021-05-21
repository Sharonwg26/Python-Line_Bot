from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('OQqOlMprRqeiXhBHSymZ45X+i7WF74swYPh3nYpgcrVezoVQQ726Eqh2e0oBORceRt+brhEoSIC6W61E4H3bxGOg4Wp51V/XsG4QW4fIkPNrb/leolZ31igBf2WZd0cTnKS86EFUUWQy2TZNgHu6ugdB04t89/1O/w1cDnyilFU=')
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

def MakeIntroduction():
    msg="您好！我是疫情小幫手，您可以輸入以下關鍵字：\n\
    '疫情'查看全台灣Covid-19疫情情況；\n \
    '量體溫'輸入您的體溫，小幫手會為您記錄；\n \
    '地區'查看您附近地區的Covid-19患者足跡；\n \
    '篩檢站'查看全台灣的篩檢站和醫院；\n \
    '疫苗'查看全台灣可施打疫苗的醫院；\n \
    '保險'查看各公司防疫保單的相關訊息；\n \
    '教學網站'查看中央大學相關的教育網站以及線上教學的軟體；\n \
    '時間提醒'可以自定義時間和事件，小幫手會提醒您哦；\n \
    '猜拳'來和小幫手玩猜拳吧XD"
    return msg

def MakePaperScissorsStone(text):
    # 石頭：0, 布：1, 剪刀：2
    if text=="石頭！":
        player=0
    elif text=="布！":
        player=1
    else:
        player=2
        
    opponent=random.randint(0,2)
    
    # 電腦：石頭, 玩家：布
    if opponent==0 and player==1:
        msg='我出石頭，你出布！\n你贏了.. ｡ﾟヽ(ﾟ´Д`)ﾉﾟ｡'
    # 電腦：石頭, 玩家：剪刀
    elif opponent==0 and player==2:
        msg='我出石頭，你出剪刀！\n我贏啦(●ˊωˋ●)ゞ'
    # 電腦：布, 玩家：石頭
    elif opponent==1 and player==0:
        msg='我出布，你出石頭！\n我贏啦(●ˊωˋ●)ゞ'
    # 電腦：布, 玩家：剪刀
    elif opponent==1 and player==2:
        msg='我出布，你出剪刀！\n你贏了.. ｡ﾟヽ(ﾟ´Д`)ﾉﾟ｡'
    # 電腦：剪刀, 玩家：石頭
    elif opponent==2 and player==0:
        msg='我出剪刀，你出石頭！\n你贏了.. ｡ﾟヽ(ﾟ´Д`)ﾉﾟ｡'
    # 電腦：剪刀, 玩家：布
    elif opponent==2 and player==1:
        msg='我出剪刀，你出布！\n我贏啦(●ˊωˋ●)ゞ'
    else:
        if opponent==0:
            msg='我們都出石頭！'
        elif opponent==1:
            msg='我們都出布！'
        else:
            msg='我們都出剪刀！'
        msg+='\n這次平手啦～d(`･∀･)b'
    return msg

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = TextSendMessage(text=event.message.text)
    # cmd = message.split(" ")
    cmd = event.message.text.split(" ")
    if cmd[0] == "介紹":
        IntroductionMsg=MakeIntroduction()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=IntroductionMsg))
        
    elif cmd[0] == "猜拳":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='剪刀石頭布！',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="石頭", text="石頭！"),
                            image_url='https://eswarupkumar.github.io/Stone-Paper-Scissor/rock.png'
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="布", text="布！"),
                            image_url='https://eswarupkumar.github.io/Stone-Paper-Scissor/paper.png'
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="剪刀", text="剪刀！"),
                            image_url='https://eswarupkumar.github.io/Stone-Paper-Scissor/scissors.png'
                        )
                    ])))
        
    elif cmd[0] == "石頭！" or cmd[0] == "布！" or cmd[0] == "剪刀！":
        PaperScissorsStoneMsg=MakePaperScissorsStone(cmd[0])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=PaperScissorsStoneMsg))
        
    else:
        else_msg = '幹嘛o( ˋωˊ )o'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=else_msg))
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
