import os
from flask import Flask, request, abort
import pandas as pd
import re

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    '6f0iOVBzeFhQKMAW2dVqAFgb+FMU5iPqO6wxB+c1m11HIncCXARKrRbPI/YI9W5SDOe6Cs8hbvGvK2CzTPH8ErsBXnRs5UMvC0abhUayHGtXrW/9aLiOh4QcSrJRc57ccQDTV/C8uBy1fiU2Nc4gigdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a228e3664a186a74e79f9b24c1f4e51b')

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


def leave(keyword):

    time = re.findall(r"\d{1,2}", keyword[2])

    if len(time) > 2:

        if keyword[2][-2:] == "上午" or keyword[2][-2:] == "下午":

            flex_msg = [
                keyword[1][4:],
                keyword[3][-3:],
                time[0]+"/"+time[1],
                time[2]+"/"+time[3],
                keyword[2][-2:],
            ]

        else:

            flex_msg = [
                keyword[1][4:],
                keyword[3][-3:],
                time[0]+"/"+time[1],
                time[2]+"/"+time[3],
                "",
            ]

    else:

        if "上午" in keyword[2][-3:] or "下午" in keyword[2][-3:]:

            flex_msg = [
                keyword[1][4:],
                keyword[3][-3:],
                time[0]+"/"+time[1],
                time[0]+"/"+time[1],
                keyword[2][-3:].strip(")"),
            ]

        else:

            if "：" in keyword[3][-3:] or ":" in keyword[3][-3:]:

                flex_msg = [
                    keyword[1][4:],
                    keyword[3][-2:],
                    time[0]+"/"+time[1],
                    time[0]+"/"+time[1],
                    "",
                ]

            else:

                flex_msg = [
                    keyword[1][4:],
                    keyword[3][-3:],
                    time[0]+"/"+time[1],
                    time[0]+"/"+time[1],
                    "",
                ]
    return flex_msg

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text = event.message.text
    if ("[請假通知]" in text):

        m = re.findall(r"\w....+", text)
        k = leave(m)
        reply_text = "姓名: "+k[0]+"\n" +\
                     "假別: "+k[1]+"\n" +\
                     "請假起始日: "+k[2]+"\n" +\
                     "請假迄止日: "+k[3]+"\n" +\
                     "時段: "+k[4]

        # "姓名: "+m[0][1]+"\n" + \
        #              "假別: "+m[2][1]+"\n" + \
        #              "請假起始日: "+m[1][1][0:-2]+"\n" + \
        #              "請假迄止日: "+m[1][1][0:-2]+"\n" + \
        #              "時段: "+m[1][1][-2:]

    if (text == "last pp"):
        with open("released.txt", "r") as f:
            for line in f.readlines():
                if "pp".upper() in line:
                    reply_text = line

    if (text == "last aos"):
        with open("released.txt", "r") as f:
            for line in f.readlines():
                if "aos".upper() in line:
                    reply_text = line

    # elif (text == "Hi" or text == "hi"):
    #     reply_text = "Hello"
    #     # Your user ID
    #
    # elif(text == "你好"):
    #     reply_text = "哈囉"
    # elif(text == "機器人"):
    #     reply_text = "叫我嗎"
    else:
        # reply_text = text
        pass

    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
