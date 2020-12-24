# -*-coding: utf-8-*-

import os
from flask import Flask, request, abort
import pandas as pd
import re
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import COMMASPACE
import base64
import psycopg2

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

    if len(time) > 4:

        flex_msg = [

            name,
            leave,
            time[0]+"/"+time[1],
            time[4]+"/"+time[5],
            period,

        ]

    elif len(time) == 4:

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


def postgresql_to_dataframe(select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1

    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()

    # We just need to turn it into a pandas dataframe
    ddd = pd.DataFrame(tupples, columns=column_names)
    return ddd

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

        time = re.findall(r"\d{1,2}", m[2])

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

            reply_text = pd.DataFrame(index=cols,
                                      data=leaves_func(m[1][3:],
                                                       leaves[leaves_intersection[0]],
                                                       time,
                                                       period_intersection[0]))

            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()
            copy_list = leaves_func(m[1][3:],
                                    leaves[leaves_intersection[0]],
                                    time,
                                    period_intersection[0])

            cursor.execute("INSERT INTO leaves_statistic VALUES (%s, %s, %s, %s, %s)",
                           (copy_list))
            conn.commit()
            # count = cursor.rowcount
            # reply_text = f"{count} Record inserted successfully into mobile table"
            cursor.close()
            conn.close()

            # reply_text = reply_text.to_string()
            # reply_text = reply_text.style.hide_index()

        else:
            reply_text = pd.DataFrame(index=cols,
                                      data=leaves_func(m[1][3:],
                                                       leaves[leaves_intersection[0]],
                                                       time,
                                                       ))
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()
            copy_list = leaves_func(m[1][3:],
                                    leaves[leaves_intersection[0]],
                                    time)
            cursor.execute("INSERT INTO leaves_statistic VALUES (%s, %s, %s, %s, %s)",
                           (copy_list))
            conn.commit()
            # count = cursor.rowcount
            # reply_text = f"{count} Record inserted successfully into mobile table"
            cursor.close()
            conn.close()
            # reply_text = reply_text.to_string()
            # reply_text = reply_text.style.hide_index()
        # reply_text = reply_text.T
        # if file does not exist write header
        # if not os.path.isfile('/app/test.csv'):
        #     reply_text.to_csv('/app/test.csv', encoding='big5', index=False)
        # reply_text = reply_text.to_string()
        # else:  # else it exists so append without writing the header
        #     reply_text.to_csv('/app/test.csv', mode='a', header=False,
        #                       encoding='big5', index=False)
        # reply_text = reply_text.to_string()

    if (text == 'csv'):

        column_names = ["姓名", "假別", "請假起始日", "請假迄止日", "時段"]

        # Execute the "SELECT *" query
        ddd = postgresql_to_dataframe(
            "select * from leaves_statistic", column_names)
        ddd.to_csv("/app/test.csv", encoding='big5', index=False)

        SUBJECT = 'Subject string'
        FILENAME = 'leaves_statistic.csv'
        FILEPATH = '/app/test.csv'
        MY_EMAIL = 'leeliao@why-not.com.tw'
        MY_PASSWORD = 'JordaN72929'
        TO_EMAIL = "leeliao@why-not.com.tw"
        SMTP_SERVER = 'smtp-mail.outlook.com'
        SMTP_PORT = 587

        you = ["leeliao@why-not.com.tw", "elinahung@why-not.com.tw"]

        # "elinahung@why-not.com.tw"

        msg = MIMEMultipart()
        msg['From'] = MY_EMAIL
        # msg['To'] = COMMASPACE.join([TO_EMAIL])
        msg['To'] = COMMASPACE.join(you)
        msg['Subject'] = SUBJECT

        part = MIMEBase('application', "octet-stream")

        part.add_header('Content-Transfer-Encoding', 'base64')
        part.add_header('Content-Disposition', 'attachment', filename=FILENAME)

        # fp = open(pdf, 'rb')
        fp = open(FILEPATH, "rb")

        # str(base64.encodebytes(fp.read()),'ascii')
        part.set_payload(str(base64.encodebytes(fp.read()), 'ascii'))
        fp.close()
        msg.attach(part)

        smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(MY_EMAIL, MY_PASSWORD)
        # smtpObj.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
        smtpObj.sendmail(MY_EMAIL, you, msg.as_string())
        smtpObj.quit()

        reply_text = "Email sent!"

    if (text == "reset db"):

        reset_table = ("""DROP TABLE leaves_statistic;""")

        create_table_query = (

            """
                CREATE TABLE leaves_statistic (
             
                    name_db TEXT NOT NULL,
                    leaves_db VARCHAR(255) NOT NULL,
                    start_time VARCHAR(255) NOT NULL,
                    end_time VARCHAR(255) NOT NULL,
                    period_db VARCHAR(255) NOT NULL
             
                );
            """

        )
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(reset_table)
        conn.commit()
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        reply_text = "DB has been reset."

    else:
        # reply_text = text
        pass

    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
