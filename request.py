import requests
from requests_html import HTML, HTMLSession

# with open('https://forum.netmarble.com/7ds_tw') as html_file:
#     source = html_file.read()
#     html = HTML(html=source)

# payload = {'username': 'Lee', 'password': 'testing'}
# r = requests.post('https://httpbin.org/post', params=payload)

session = HTMLSession()
r = session.get('https://forum.netmarble.com/7ds_tw')
r.html.render(sleep=3, keep_page=True, scrolldown=1)

# print(r.html.html)
news_list = r.html.find('a.title')
# news_list = r.html.links
# news = news_list.find('')
# print(news_list.attr)
for i in news_list:
    print(i.text)
