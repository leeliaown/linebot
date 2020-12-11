import pandas as pd


def process_string(keyword):
    flex_msg = {
        'name': keyword[0:3],
        'leave': keyword[0:6],
        'leave_time': keyword[0:10],
        'period': keyword[0:15]
    }

    return flex_msg


s = "[請假通知] \
姓名: joeytseng \
請假日期: 12/11 (五)下午 \
請假事由: 特休 \
直屬主管: chris \
職務代理人: chris \
有急事請Line 或 電話聯絡，謝謝 !"

# print(process_string(s))
flex_msg = {
    'name': s[0:3],
    'leave': s[0:6],
    'leave_time': s[0:10],
    'period': s[0:15]

}

df = pd.Series(data=flex_msg)

print(df.head())
