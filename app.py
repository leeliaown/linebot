import os
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text = event.message.text
    if (text == "last pp"):
        with open("released.txt", "r")as f:
            for line in f.readlines():
                if "pp" in line:
                    reply_text = line

    elif (text == "Hi" or text == "hi"):
        reply_text = "Hello"
        # Your user ID

    elif(text == "你好"):
        reply_text = "哈囉"
    elif(text == "機器人"):
        reply_text = "叫我嗎"
    else:
        reply_text = text

    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
