# Python - Line Bot

---

## 疫情小幫手 架構

----

### 平台 — LINE
疫情小幫手 是這個 ChatBot 的名稱，而 疫情小幫手 是一個建立在 LINE 平台之上的 ChatBot。之所以選擇以 LINE 為平台，主要原因也是台灣對於 LINE 的高度依賴性所致。


---

### 架構 — Django
能夠實現 LINE Bot 的方式有很多，由於我是參照書上指示進行建構，因此便以 Django 為 疫情小幫手 的設計架構。


---

### 伺服器 — heroku
目前非自架伺服器的選擇大多是 ngrok 以及 heroku，前者重新執行後都會改變網址，對於要常態性使用上會相對不是這麼好用。
heroku 有免費的方案，在架構上只要滿足其要求，往後的更動都只須調整代碼即可，其餘的都不太需要多操心，可以算是初級 LINE Bot 開發者的首選。


---

### 資料擷取 — 疫情指揮中心 API
現階段 疫情小幫手 開發出來的功能有二 :
1. 當日確診人數
2. 地區
   詢部分接收到訊息後確認待查詢縣市後依靠中央氣象局公開資料 API 擷取「36小時天氣預報資料」資訊，將我們要的縣市資訊抓出來再回覆給使用者。

[新冠肺炎 COVID-19 疫苗接種院所查詢](https://tools.heho.com.tw/covid-19-vaccine/)
---

### Google YouTube API
增加了可以查詢當日疫情記者會的部分，以疫情指揮中心的分析為爬蟲對象。
利用 google API 可以用簡單的方式來取得 YouTube 內容。
    
    
>麻煩大家填寫 [name=Sharonwg26] 
    
    
---

## 功能
1. 疫情 回復多少
2. 量體溫：輸入體溫
3. 地區 比對足跡
4. 篩檢站 附近醫院
5. 疫苗 可施打醫院
6. 時間提醒 自定義
7. 教學網站 相關教學網站連結
8. 保險 防疫保單種類
9. 猜拳

[可以的话文字可以加一些emoji或者表情，看起来比较有趣]


---

## 分工
* 安安
    * 保险
    * 筛检站
    * 时间提醒 （X）
* 丁丁
    * 教学网站
    * 縣市今日疫情（新增確診）
* 沂萱
    * 疫情：全球疫情（累計、死亡）、台灣疫情（累計、本土、境外、死亡）、今日疫情（累計、本土、境外）、縣市疫情（累計）
    * 猜拳
    * 🐷
    > ???
* 軒媚
    * 疫苗
    * 量體溫
    * 天氣（氣象局API）

---

## Line Bot
1. Channel secret 
    `69a5b0ff850e58d346a7695507d98177`
2. Channel access token
```
OQqOlMprRqeiXhBHSymZ45X+i7WF74swYPh3nYpgcrVezoVQQ726Eqh2e0oBORceRt+brhEoSIC6W61E4H3bxGOg4Wp51V/XsG4QW4fIkPNrb/leolZ31igBf2WZd0cTnKS86EFUUWQy2TZNgHu6ugdB04t89/1O/w1cDnyilFU=
```
3. [中央氣象局API授權碼](https://opendata.cwb.gov.tw/user/authkey)
```
CWB-E5F5EFC0-30D2-43E6-B9C5-DDC64B24FA74
```
---

![](https://i.imgur.com/sFhZgIx.png)
* 感觉大家可能会需要这个


---

## Code
* 將程式碼推上 Heroku，如果有跳出錯誤請重新輸入
```
git add .
git commit -m "Add code"
git push -f heroku main
```


----

### 基礎連接
```python=
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

```


----

### 爬爬爬
```python=
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests

response = request.get("https://covid-19.nchc.org.tw")
soup = BeautifulSoup(response.content, "html.parser")
newly_increased = soup.find('h1', {'class': 'country_confirmed mb-1 text-success'}).getText()

print(newly_increased)
```


---

## 參考

* [[Flask – LINE Bot 教學] 事前準備篇 (一)](https://www.maxlist.xyz/2020/11/16/flask-line-bot-pre-set/)
* [LineBot+Python，輕鬆建立聊天機器人](https://blackmaple.me/line-bot-tutorial/)
* [LINE Messaging API SDK for Python](https://github.com/line/line-bot-sdk-python)
* [Python Telegram Bot 教學 (by 陳達仁)](https://hackmd.io/@truckski/HkgaMUc24?type=view)

