#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from bs4 import BeautifulSoup
import random
import requests
import json

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('OQqOlMprRqeiXhBHSymZ45X+i7WF74swYPh3nYpgcrVezoVQQ726Eqh2e0oBORceRt+brhEoSIC6W61E4H3bxGOg4Wp51V/XsG4QW4fIkPNrb/leolZ31igBf2WZd0cTnKS86EFUUWQy2TZNgHu6ugdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('69a5b0ff850e58d346a7695507d98177')

cities = ['基隆市','嘉義市','臺北市','台北市','嘉義縣','新北市','臺南市','台南市','桃園縣','高雄市','新竹市','屏東縣','新竹縣','臺東縣','台東縣','苗栗縣','花蓮縣','臺中市','台中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']

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
    msg = "我是疫情小幫手，您可以輸入以下關鍵字：\n\n"
    msg += "✨疫情：\n    查看全台灣Covid-19疫情情況😈\n\n" 
    msg += "✨量體溫：\n    輸入您的體溫🌡\n\n"
    msg += "✨篩檢站：\n    查看全台灣的篩檢站和醫院🏥\n\n"
    #msg += "✨疫苗：\n    查看全台灣可施打疫苗的醫院💉\n\n"
    msg += "✨保險：\n    查看各公司防疫保單的相關訊息💰\n\n"
    msg += "✨防疫專線：\n    查看防疫專線和各縣市服務專線☎️\n\n"
    msg += "✨教學網站：\n    觀看教育網站以及線上教學📖\n\n"
    msg += "✨天氣：\n    查看當日氣溫🌦\n\n"
    msg += "✨猜拳：\n    來和小幫手玩猜拳吧✌️👊✋\n💕💕💕"
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


# 台灣縣市確診
def GetCityPandemic(city):
    # 累計確診
    url = 'https://spreadsheets.google.com/feeds/cells/1UVnq9a1zVIfygplsbOjOtMX2Bu6aUfet1PwN3MOM7bk/1/public/full?alt=json'
    reqsjson = requests.get(url).json()
    reqsjson = reqsjson["feed"]["entry"]
    target_city = "查詢格式為: 縣市疫情 縣市。\n（縣市名後請務必加上「縣/市」）"
    index = 0

    for item in reqsjson:
        if item["gs$cell"]["inputValue"] == city:
             cityPandemic = reqsjson[index + 1]["gs$cell"]["inputValue"]
             cityPandemic = city+"累計確診："+cityPandemic
             
             #---------------丁-县市新增------------------#
             url1 = 'https://covid-19.nchc.org.tw'
             html = requests.get(url1, verify=False)
             html.encoding = 'UTF-8'
             sp = BeautifulSoup(html.text, "html.parser")

             citys = sp.find_all('button', class_='btn btn-success btn-lg')#城市名
             new_confirm = sp.find_all('span', style='font-size: 0.8em;')#城市新增
             Citys = []
             New_confirm = []

             for i in range(0, len(citys)):
                 Citys.append(citys[i].get_text())

             for i in range(4, len(citys) + 4):
                 New_confirm.append(new_confirm[i].get_text())

             for i in range(0, len(Citys)):
                 Citys[i] = Citys[i].split()
                 New_confirm[i] = New_confirm[i].split()

             for i in range(0, len(Citys)):
                 if city == Citys[i][0]:
                     cityPandemic += "\n今日新增：" + "".join(New_confirm[i]) + "\n(*為矯正回歸確診數)"
             #---------------丁-县市新增------------------#
             return cityPandemic
        
        index += 1

    return target_city

                  
# 體溫
def body_temperature(num):
    if num>37.5:
        msg='發燒了，如有接觸史，快點去醫院喔!!!'
    else:
        msg='一切正常 👍👍👍'
    return msg


# 教學網站
def MakeWeb():
    msg="* 以下是中央大學相關的教育網站唷~\n\
    \r 🌟ncueeclass: \n\
    \r   https://ncueeclass.ncu.edu.tw/ \n \
    \r 🌟portal: \n\
    \r   https://portal.ncu.edu.tw/ \n \
    \r\n\
    * 以下是一些常用的遠距教學軟體哦： \n \
    \r 🌟Google Meet: \n\
    \r   https://meet.google.com/ \n \
    \r 🌟Zoom:（雖然被Ban了，不過偶爾還是會使用到）\n\
    \r   https://zoom.us/zh-tw/meetings.html\n \
    小幫手有幫到你嘛,嘻嘻ヾ(✿ﾟ▽ﾟ)ノ"
    return msg


# 天氣
def MakeAQI(station):
    end_point = "http://opendata.epa.gov.tw/webapi/api/rest/datastore/355000000I-000259?filters=SiteName eq '" + \
        station + "'&sort=SiteName&offset=0&limit=1000"

    data = requests.get(end_point)
    AQImsg = ""

    if data.status_code == 500:
        return "無 AQI 資料"
    else:
        AQIdata = data.json()["result"]["records"][0]
        AQImsg += "AQI = " + AQIdata["AQI"] + "\n"
        AQImsg += "PM2.5 = " + AQIdata["PM2.5"] + " μg/m3\n"
        AQImsg += "PM10 = " + AQIdata["PM10"] + " μg/m3\n"
        AQImsg += "空品：" + AQIdata["Status"]
        return AQImsg


def GetWeather(station):
    token = 'CWB-E5F5EFC0-30D2-43E6-B9C5-DDC64B24FA74'
    end_point = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=" + token

    data = requests.get(end_point).json()
    data = data["records"]["location"]

    target_station = "not found"
    for item in data:
        if item["locationName"] == str(station):
            target_station = item
    return target_station


def MakeWeather(station):
    WeatherData = GetWeather(station)
    if WeatherData == "not found":
        return False
    WeatherData = WeatherData["weatherElement"]
    msg = "天氣報告 - " + station
    msg += "\n\n氣溫 = " + WeatherData[3]["elementValue"] + "℃\n"
    msg += "濕度 = " + \
        str(float(WeatherData[4]["elementValue"]) * 100) + "% RH\n"

    msg += MakeAQI(station)
    return msg
"""
def get(city):
    token = 'CWB-E5F5EFC0-30D2-43E6-B9C5-DDC64B24FA74'
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(city)
    Data = requests.get(url).json()
    Data = (json.dumps(Data.text,ensure_ascii=False))['records']['location'][0]['weatherElement']
    res = json.load(open('card.json','r',encoding='utf-8'))
    print(Data)
    for j in range(3):
        bubble = json.load(open('bubble.json','r'),encoding='utf-8')
        # title
        bubble['body']['contents'][0]['text'] = city + '未來 36 小時天氣'
        # time
        bubble['body']['contents'][1]['contents'][0]['text'] = '{} ~ {}'.format(Data[0]['time'][j]['startTime'][5:-3],Data[0]['time'][j]['endTime'][5:-3])
        # weather
        bubble['body']['contents'][3]['contents'][1]['contents'][1]['text'] = Data[0]['time'][j]['parameter']['parameterName']
        # temp
        bubble['body']['contents'][3]['contents'][2]['contents'][1]['text'] = '{}°C ~ {}°C'.format(Data[2]['time'][j]['parameter']['parameterName'],Data[4]['time'][j]['parameter']['parameterName'])
        # rain
        bubble['body']['contents'][3]['contents'][3]['contents'][1]['text'] = Data[1]['time'][j]['parameter']['parameterName']
        # comfort
        bubble['body']['contents'][3]['contents'][4]['contents'][1]['text'] = Data[3]['time'][j]['parameter']['parameterName']
        res['contents'].append(bubble)
"""
#保險
def Insurance():
    response = requests.get( "https://www.phew.tw/article/cont/phewpoint/current/news/11217/2021051211217")
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("p", limit=20)
    content = ""
    for card in cards:
        title = card.find("span",{'style':"color:#0000CD;"})
        if title == None:
           continue 
        title = card.find("span",{'style':"color:#0000CD;"}).getText()
        detail = card.select_one("span", {'style':"font-size:20px;"})
        if detail == None:
            continue
        detail = card.select_one("span", {'style':"font-size:20px;"}).getText()
        if detail[len(detail)-2] == '售' and detail[len(detail)-3] == '停':
            continue
        content += f"✨{title} ✨\n{detail}\n\n"
    return content

#篩檢站
def Screeningstation(city):
    response = requests.get("https://udn.com/news/story/122173/5472099")
    city = '\n' + city
    soup = BeautifulSoup(response.text, "html.parser")
    datas = soup.find_all("p")
    content=""
    content += city+ "👻\n"
    start = 0
    for data in datas:
        detail = data.getText()
        if len(detail) >= 50 or len(detail) < 2:
            continue
        if detail == city:
            start = start + 1
            continue
        if start == 0:
            continue
        
        if len(detail) == 4 and detail != city:
            break
        content += f"{detail}"
        
    return content

#疫情專線
def MakePhonecall():
    msg="* 以下是全國的防疫專線唷~\n\
    \r 🌟安心專線：1925 \n \
    \r  服務時間：週一至週日，24小時服務專線 \n \
    \r 🌟疾病管制署防疫專線：1922 \n \
    \r  服務時間：週一至週日，24小時服務專線 \n \
    \r 🌟全國疫情免付費通報專線：0800-024-582 \n \
    \r  服務時間：週一至週日，24小時服務專線 \n \
    \r 🌟安心專線：1925 \n \
    \r  服務時間：週一至週日，24小時服務專線 \n \
    \r 🌟防疫补偿金：1957 \n \
    \r  服務時間：週一至週日，24小時服務專線 \n \
    \r\n \
    \r  各縣市服務專線請您參考以下網址：\n \
    \r  https://www.cdc.gov.tw/Category/Page/XRPe-3X_vQ0BmYLrvwruSw\n \
    小幫手有幫到你嘛～嘻嘻💗"
    return msg

# 猜拳
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    cmd = event.message.text.split(" ")
    if cmd[0] == "介紹":
        IntroductionMsg=MakeIntroduction()
        SendMsg=[TextSendMessage(text=IntroductionMsg),
                 StickerSendMessage(package_id=1, sticker_id=2)]
        line_bot_api.reply_message(event.reply_token, SendMsg)
    elif cmd[0]== "疫情":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='請選擇🐾',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="全球疫情😷", text="全球疫情")                            
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="台灣疫情😷", text="台灣疫情")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="今日疫情😷", text="今日疫情")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="縣市疫情😷", text="縣市疫情 (縣市)")
                        )
                    ])))
        
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
        city = cmd[1]
        city = city.replace('台','臺')
        CityPandemicMsg = GetCityPandemic(city)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=CityPandemicMsg))
        
    elif cmd[0] == "量體溫":
        temperature=body_temperature(float(cmd[1]))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=temperature))
        
    elif cmd[0] == "教學網站":
        carousel_template_message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://news.idea-show.com/wp-content/uploads/2020/04/國立中央大學.jpg',
                        action=URIAction(
                            label='NCU Portal',
                            uri='https://portal.ncu.edu.tw/'
                        ),
                    ),
                    ImageCarouselColumn(
                        image_url='https://ncueeclass.ncu.edu.tw/sysdata/attach/p.4//3d614763f288bfab5feebb6c36cb49bd.png',
                        action=URIAction(
                            label='NCU ee-class',
                            uri='https://ncueeclass.ncu.edu.tw/'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-05-512.png',
                        action=URIAction(
                            label='Google Meet',
                            uri='https://meet.google.com/'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://www.pngarts.com/files/7/Zoom-Logo-PNG-Free-Download.png',
                        action=URIAction(
                            label='Zoom',
                            uri='https://zoom.us/zh-tw/meetings.html'
                        )
                    )
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token,carousel_template_message)
        '''
        Carousel_template = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.ncu.edu.tw/assets/thumbs/pic/df1dfaf0f9e30b8cc39505e1a5a63254.png',
                        title='NCU portal',
                        actions=[
                            URITemplateAction(
                                label='https://portal.ncu.edu.tw/',
                                uri='https://portal.ncu.edu.tw/'
                            )   
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fncueeclass.ncu.edu.tw%2Fcourse%2F5139&psig=AOvVaw0dfl7GXvLSVUyHG5XJlzIC&ust=1622295317848000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCIiG6qa_7PACFQAAAAAdAAAAABAD',
                        title='ncueeclass',
                        actions=URITemplateAction(
                            label='https://ncueeclass.ncu.edu.tw/',
                            uri='https://ncueeclass.ncu.edu.tw/'
                        )
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Ftw.news.yahoo.com%2F%25E5%25A6%2582%25E4%25BD%2595%25E4%25BB%25A5google%25E6%2597%25A5%25E6%259B%2586%25E9%2596%258B%25E5%2595%259Fgoogle-meet%25E8%25A6%2596%25E8%25A8%258A%25E6%259C%2583%25E8%25AD%25B0-133250711.html&psig=AOvVaw1PK-DKPV5Mu3kmBY758KeA&ust=1622295565077000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJCGyInA7PACFQAAAAAdAAAAABAD',
                        title='Google Meet',
                        actions=URITemplateAction(
                                label='https://meet.google.com/',
                                uri='https://meet.google.com/'
                        )
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fmashdigi.com%2Fzoom-updated-for-zoom-bombing%2F&psig=AOvVaw0F3B34WXcnhmD5-p1PraSP&ust=1622295743950000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCKDDnN_A7PACFQAAAAAdAAAAABAD',
                        title='Zoom',
                        text='雖然被Ban了，不過偶爾還是會使用到呢',
                        actions=URITemplateAction(
                                label='https://zoom.us/zh-tw/meetings.html',
                                uri='https://zoom.us/zh-tw/meetings.html'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
        '''
        
        #WebMsg = MakeWeb()
        #SendMsg = [TextSendMessage(text=WebMsg),
                  # StickerSendMessage(package_id=1, sticker_id=4)]
        #line_bot_api.reply_message(event.reply_token, SendMsg)
    
    elif cmd[0] == "天氣":
        city = cmd[1]
        city = city.replace('台','臺')
        WeatherMsg = MakeWeather(city)
        if not WeatherMsg:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="查詢格式為: 天氣 氣象站"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=WeatherMsg))
    elif(cmd == 'location'):
        message=event.message.text
        city = event.message.address[5:8].replace('台','臺')
        res = get(city)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(city + '未來 36 小時天氣預測',res))         
    
    elif cmd[0] == "保險":
        InsuranceInformation = Insurance()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=InsuranceInformation))
    
    elif cmd[0] == "防疫專線":
        PhoneMsg = MakePhonecall()
        SendMsg = TextSendMessage(text=PhoneMsg)
        line_bot_api.reply_message(event.reply_token, SendMsg)
    
    elif cmd[0] == "篩檢站":
        city = cmd[1]
        #city = city.replace('臺','台')
        if(not (city in cities)):
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="查詢格式為: 篩檢站 縣市"))
        else:
            station = Screeningstation(city)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=station))
        
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
        SendMsg = MakePaperScissorsStone(cmd[0])+"\n\n再來一場嗎(*ˇωˇ*人)"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=SendMsg,
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
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="不玩啦", text="不玩啦"),
                            image_url='https://image.pngaaa.com/302/49302-middle.png'
                        )
                    ])))
    
    elif cmd[0]== "不玩啦":
        ByeByeMsg="好吧( ˘•ω•˘ ) 下次見！"
        SendMsg=[TextSendMessage(text=ByeByeMsg),
                 StickerSendMessage(package_id=11537, sticker_id=52002771)]
        line_bot_api.reply_message(event.reply_token, SendMsg)
        
    else:
        else_msg = '幹嘛o( ˋωˊ )o'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=else_msg))
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
