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
    result = requests.post(url='https://www.medtronic-pro.vip/webHT6665zzz696/huilv', data=value)
    time.sleep(4)
    print(result.text)
    file_handle=open('article.txt',mode='w',encoding='utf-8')
    detail = str(result.text)
    file_handle.write(detail)
    file_handle.close()
    return result.text
    try:
        data = json.loads(result.text)
        print(data['data'])
        return data['data']
    except:
        print('错误')
        traceback.print_exc()

def getContentBuyUrl(url,auth,auths):

    content = url_content(url)
    #print(content)
    lists = content.find_all(class_='listing-widget-33')
    for listInfo in lists:
        try:
            print(listInfo)
            detailUrlContent = listInfo.find(class_='listing-overlay')
            detailUrlEnd = detailUrlContent.attrs['href']
            cover = baseUrl+listInfo.find(class_='lazyload').attrs['src']
            print(detailUrlEnd)
            title = detailUrlContent.attrs['title']
            print(title)
            detailUrl = baseUrl+detailUrlEnd
            detailContentHtml = url_content(detailUrl);
            detailContent = detailContentHtml.find(class_="article-detail-content-container").find_all('p')
            content = []
            for p in detailContent:
                print(p)
                if 'id' in p.attrs :
                    continue
                if "相關文章" in p.text:
                    break
                content.append(str(p))
            
            print(str("".join(content)))
            result = postNovelMethod({'title':title,'content':str("".join(content)),'auth':auth,'auths':auths,'cover':cover,'url':detailUrlEnd})
            print(result)
            if result != '1':
                return True
                
        
        except:
            print('错误')
            continue

                
    

# novel = postNovelMethod({'title':'title','cate':'1','pic':'pic','author':'author','content':'content','url':'url'})

# postChapterMethod({'novel':novel,'sort':1,'name':'name','content':'content','url':'url'})
baseUrl = 'https://inews.hket.com'
cjUrl = 'https://inews.hket.com/sran009/%E5%8D%B3%E5%B8%82%E8%B2%A1%E7%B6%93?mtc=80042'
kjUrl = 'https://inews.hket.com/sran010/%E7%A7%91%E6%8A%80?mtc=20080'
gpUrl = 'https://inews.hket.com/sran012/%E5%95%86%E6%A5%AD?mtc=20080'
gjUrl = 'https://inews.hket.com/sran011/%E5%9C%8B%E9%9A%9B?mtc=20080'
while True:

    try:
        print("start cjxw ")
        getContentBuyUrl(cjUrl,'財經新聞',30)
        print("start gjyw ")
        getContentBuyUrl(gjUrl,'國際要聞',64)
        print("start gpzx ")
        getContentBuyUrl(gpUrl,'股票資訊',63)
        print("start kjxw ")
        getContentBuyUrl(kjUrl,'科技新聞',62)
        print("over start sleep")
        time.sleep(3600)
    except:
        print('错误')
        time.sleep(600)
    #exit()