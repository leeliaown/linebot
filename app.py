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


leaves = {

    "特休": "特休",
    "特休假": "特休",
    "病假回診": "病假",
    "病假": "病假",
    "陪產假": "陪產假",
    "生理假": "生理假",
    "事假": "事假",
    "身體不適": "病假",
    "回診": "病假",
    "休假": "特休",
}

periods = {"上午": "上午", "下午": "下午"}

cols = ['姓名', '假別', '請假起始日', '請假迄止日', '時段', ]


def leaves_func(name, leave=0, time=0, period=""):

    if len(time) == 4:

        flex_msg = [

            name,
            leave,
            time[0]+"/"+time[1],
            time[2]+"/"+time[3],
            period,
        ]

    elif len(time) == 3:

        flex_msg = [

            name,
            leave,
            time[0]+"/"+time[1],
            time[0]+"/"+time[2],
            period,
        ]

    else:

        if period:

            flex_msg = [

                name,
                leave,
                time[0]+"/"+time[1],
                time[0]+"/"+time[1],
                period,
            ]

        else:

            flex_msg = [

                name,
                leave,
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
        period = re.findall(r"\b\w{1,2}\b", text)

        period_set = set(period)
        periods_set = set(periods)
        period_intersection = list(period_set.intersection(periods_set))

        time = re.findall(r"\d{1,2}", text)

        name = re.findall(r"([a-zA-z].*(\S|\s)[a-zA-z].*)", text)

        leave_1 = re.findall(r"\b[^\W\sa-zA-Z0-9]{2,4}\b", text)
        leave_set = set(leave_1)
        leaves_set = set(leaves)
        leaves_intersection = list(leave_set.intersection(leaves_set))

        k = leaves_func(name,
                        leaves[leaves_intersection[0]],
                        time,
                        period_intersection,
                        )

        if period_intersection:
            # reply_text = "姓名: "+k[0]+"\n" +\
            #              "假別: "+k[1]+"\n" +\
            #              "請假起始日: "+k[2]+"\n" +\
            #              "請假迄止日: "+k[3]+"\n" +\
            #              "時段: "+k[4]
            reply_text = pd.DataFrame(index=cols,
                                      data=leaves_func(m[1][3:],
                                                       leaves[leaves_intersection[0]],
                                                       time,
                                                       period_intersection[0]))

            reply_text = reply_text.to_string()
            # reply_text = reply_text.style.hide_index()

        else:
            reply_text = pd.DataFrame(index=cols,
                                      data=leaves_func(m[1][3:],
                                                       leaves[leaves_intersection[0]],
                                                       time,
                                                       ))

            reply_text = reply_text.to_string()
            # reply_text = reply_text.style.hide_index()

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
