import requests
import os
from bs4 import BeautifulSoup
import json
import random
import time
import sys

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'content-type': 'charset=utf8',
    'cookie': 'home_lang=cn; admin_lang=cn; PHPSESSID=muaj4rt89ntduqglhuvjbgf922; Hm_lvt_807902317c8d34e6764b79204c91d413=1687137049; Hm_lpvt_807902317c8d34e6764b79204c91d413=1687152432'
}


def url_content(url, proxies=False, i=0):
    print(url)
    time.sleep(random.randrange(2))
    if i > 10:
        return False
    try:
        response = requests.get(url, timeout=25, headers=DEFAULT_REQUEST_HEADERS)
    except:
        print('超时')
        return url_content(url, False, i + 1)
    response.encoding = "utf-8"
    list_txt = BeautifulSoup(response.text, 'html.parser')
    return list_txt


def postNovelMethod(value):
    result = requests.post(url='http://211.49.226.243:8686/index/article/api', data=value)
    time.sleep(4)
    print(result.text)
    file_handle=open('article.txt',mode='w',encoding='utf-8')
    detail = str(result.text)
    file_handle.write(detail)
    file_handle.close()
    return True
    try:
        data = json.loads(result.text)
        print(data['data'])
        return data['data']
    except:
        print('错误')
        traceback.print_exc()

# novel = postNovelMethod({'title':'title','cate':'1','pic':'pic','author':'author','content':'content','url':'url'})

# postChapterMethod({'novel':novel,'sort':1,'name':'name','content':'content','url':'url'})
baseUrl = 'https://www.brcns.cn'
url = 'https://www.npr.org/sections/business/'
while True:
    content = url_content(url)
    print(content)
    lists = content.find_all('article')
    for listInfo in lists:
        try:
            print(listInfo)
            detailUrlEnd = listInfo.find(class_='title').find('a').attrs['href']
            cover = listInfo.find('picture').find('img').attrs['src']
            print(detailUrlEnd)
            title = listInfo.find(class_='title').text
            print(title)
            detailUrl = detailUrlEnd
            detailContentHtml = url_content(detailUrl);
            detailContent = detailContentHtml.find(id="storytext")
            auth = detailContentHtml.find(class_="byline__name").text
            print(auth)
            ctime = detailContentHtml.find("time").attrs['datetime']
            print(ctime)
            postNovelMethod({'title':title,'content':str(detailContent),'auth':auth,'cover':cover,'url':detailUrlEnd,'ctime':ctime})
        except:
            continue
        #exit()
    time.sleep(3600)
    #exit()