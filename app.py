from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random
import requests
import json

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
    '全球疫情'查看全球Covid-19疫情；\n \
    '台灣疫情'查看台灣Covid-19疫情；\n \
    '今日疫情'查看台灣今日Covid-19疫情；\n \
    '縣市疫情 縣市名'查看您輸入地區的Covid-19疫情；\n \
    '量體溫'輸入您的體溫，小幫手會為您記錄；\n \
    '篩檢站'查看全台灣的篩檢站和醫院；\n \
    '疫苗'查看全台灣可施打疫苗的醫院；\n \
    '保險'查看各公司防疫保單的相關訊息；\n \
    '教學網站'查看中央大學相關的教育網站以及線上教學的軟體；\n \
    '時間提醒'可以自定義時間和事件，小幫手會提醒您哦；\n \
    '猜拳'來和小幫手玩猜拳吧XD"
    return msg

def MakeWeb():
    msg="以下是中央大學相關的教育網站唷~\n\
    1.ncueeclass: https://ncueeclass.ncu.edu.tw/ \n \
    2.portal: https://portal.ncu.edu.tw/ \n \
    以下是一些常用的遠距教學軟體哦： \n \
    1.Google meeting: https://meet.google.com/ \n \
    2.Zoom:  https://zoom.us/zh-tw/meetings.html  （雖然被Ban了，不過偶爾還是會使用到）    \n \
    小幫手有幫到你嘛,嘻嘻ヾ(✿ﾟ▽ﾟ)ノ"
    return msg

def MakePaperScissorsStone(text):
    # 石頭：0, 布：1, 剪刀：2
    if text=="石頭👊！":
        player=0
    elif text=="布✋！":
        player=1
    else:
        player=2
        
    opponent=random.randint(0,2)
    
    # 電腦：石頭, 玩家：布
    if opponent==0 and player==1:
        msg='我出👊，你出✋！\n你贏了.. ｡ﾟヽ(ﾟ´Д`)ﾉﾟ｡'
    # 電腦：石頭, 玩家：剪刀
    elif opponent==0 and player==2:
        msg='我出👊，你出✌️！\n我贏啦(●ˊωˋ●)ゞ'
    # 電腦：布, 玩家：石頭
    elif opponent==1 and player==0:
        msg='我出✋，你出👊！\n我贏啦(●ˊωˋ●)ゞ'
    # 電腦：布, 玩家：剪刀
    elif opponent==1 and player==2:
        msg='我出✋，你出✌️！\n你贏了.. ｡ﾟヽ(ﾟ´Д`)ﾉﾟ｡'
    # 電腦：剪刀, 玩家：石頭
    elif opponent==2 and player==0:
        msg='我出✌️，你出👊！\n你贏了.. ｡ﾟヽ(ﾟ´Д`)ﾉﾟ｡'
    # 電腦：剪刀, 玩家：布
    elif opponent==2 and player==1:
        msg='我出✌️，你出✋！\n我贏啦(●ˊωˋ●)ゞ'
    else:
        if opponent==0:
            msg='我們都出👊！'
        elif opponent==1:
            msg='我們都出✋！'
        else:
            msg='我們都出✌️！'
        msg+='\n這次平手啦～d(`･∀･)b'
    return msg

# 全球疫情
def GetGlobalPandemic():
    url ='https://spreadsheets.google.com/feeds/cells/1UVnq9a1zVIfygplsbOjOtMX2Bu6aUfet1PwN3MOM7bk/1/public/full?alt=json'
    reqsjson = requests.get(url).json()
    reqsjson = reqsjson["feed"]["entry"]
    globalpandemic = "全球確診："+str(format(int(reqsjson[5]["gs$cell"]["inputValue"]),','))+"\n死亡："+str(format(int(reqsjson[6]["gs$cell"]["inputValue"]),','))
    return globalpandemic

# 台灣疫情
def GetTaiwanPandemic():
    url ='https://spreadsheets.google.com/feeds/cells/1UVnq9a1zVIfygplsbOjOtMX2Bu6aUfet1PwN3MOM7bk/1/public/full?alt=json'
    reqsjson = requests.get(url).json()
    reqsjson = reqsjson["feed"]["entry"]
    # 台灣累計確診 reqsjson[11]["gs$cell"]["inputValue"]
    # 台灣累計本土確診 reqsjson[67]["gs$cell"]["inputValue"]
    # 台灣累計境外移入 reqsjson[69]["gs$cell"]["inputValue"]
    # 台灣累計死亡 reqsjson[79]["gs$cell"]["inputValue"]
    taiwanpandemic = "台灣累計確診："+reqsjson[11]["gs$cell"]["inputValue"]+"\n本土案例："+reqsjson[67]["gs$cell"]["inputValue"]+"\n境外移入："+reqsjson[69]["gs$cell"]["inputValue"]+"\n死亡："+reqsjson[79]["gs$cell"]["inputValue"]
    return taiwanpandemic

# 今日台灣疫情
def GetTodayPandemic():
    url ='https://spreadsheets.google.com/feeds/cells/1UVnq9a1zVIfygplsbOjOtMX2Bu6aUfet1PwN3MOM7bk/1/public/full?alt=json'
    reqsjson = requests.get(url).json()
    reqsjson = reqsjson["feed"]["entry"]
    todaypandemic = "今日新增："+reqsjson[13]["gs$cell"]["inputValue"]+"\n本土案例："+reqsjson[15]["gs$cell"]["inputValue"]+"\n境外移入："+reqsjson[17]["gs$cell"]["inputValue"]
    return todaypandemic

# 台灣縣市累計確診
def GetCityPandemic(city):
    url ='https://spreadsheets.google.com/feeds/cells/1UVnq9a1zVIfygplsbOjOtMX2Bu6aUfet1PwN3MOM7bk/1/public/full?alt=json'
    reqsjson = requests.get(url).json()
    reqsjson = reqsjson["feed"]["entry"]
    target_city = "輸入錯誤，請重新輸入。\n（縣市名後請務必加上「縣/市」）"
    index = 0
    
    for item in reqsjson:
            if item["gs$cell"]["inputValue"] == city:
                return reqsjson[index+1]["gs$cell"]["inputValue"]
            index += 1

    return target_city


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    cmd = event.message.text.split(" ")
    if cmd[0] == "介紹":
        IntroductionMsg=MakeIntroduction()
        SendMsg=[TextSendMessage(text=IntroductionMsg),
                 StickerSendMessage(package_id=1, sticker_id=2)]
        line_bot_api.reply_message(event.reply_token, SendMsg)
        
    elif cmd[0] == "教學網站":
        WebMsg = MakeWeb()
        SendMsg = [TextSendMessage(text=WebMsg),
                   StickerSendMessage(package_id=1, sticker_id=4)]
        line_bot_api.reply_message(event.reply_token, SendMsg)
        
    elif cmd[0] == "猜拳":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='剪刀石頭布！',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="石頭", text="石頭👊！"),
                            image_url='https://eswarupkumar.github.io/Stone-Paper-Scissor/rock.png'
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="布", text="布✋！"),
                            image_url='https://eswarupkumar.github.io/Stone-Paper-Scissor/paper.png'
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="剪刀", text="剪刀✌️！"),
                            image_url='https://eswarupkumar.github.io/Stone-Paper-Scissor/scissors.png'
                        )
                    ])))
        
    elif cmd[0] == "石頭👊！" or cmd[0] == "布✋！" or cmd[0] == "剪刀✌️！":
        PaperScissorsStoneMsg = MakePaperScissorsStone(cmd[0])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=PaperScissorsStoneMsg))
    
    elif cmd[0]== "全球疫情":
        GlobalPandemicMsg = GetGlobalPandemic()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=GlobalPandemicMsg))
        
    elif cmd[0]== "台灣疫情":
        TaiwanPandemicMsg = GetTaiwanPandemic()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=TaiwanPandemicMsg))
        
    elif cmd[0]== "今日疫情":
        TodayPandemicMsg = GetTodayPandemic()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=TodayPandemicMsg))
        
    elif cmd[0]== "縣市疫情":
        CityPandemicMsg = GetCityPandemic(cmd[1])
        if CityPandemicMsg != "輸入錯誤，請重新輸入。\n（縣市名後請務必加上「縣/市」）":
            CityPandemicMsg = cmd[1]+":"+CityPandemicMsg+"例"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=CityPandemicMsg))
        
    else:
        else_msg = '幹嘛o( ˋωˊ )o'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=else_msg))
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
