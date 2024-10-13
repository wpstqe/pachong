import requests
from bs4 import BeautifulSoup
import json
import random
import time
import pymysql
import traceback
import sys
import threading
import oss2
import os
import hashlib

USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': random.choice(USER_AGENT_LIST),
    'content-type': 'charset=utf8'
}
def ossUpload(url,content):
    # 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
    auth = oss2.Auth('LTAI5tKyeboCQB9DoN32wz5oB','pbbIBUowDjFrrw9Ew3JhuqeFsYVTGa1yz')
    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # 填写Bucket名称。
    bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'my-novel-info')

    # 上传文件。
    # 如果需要在上传文件时设置文件存储类型（x-oss-storage-class）和访问权限（x-oss-object-acl），请在put_object中设置相关Header。
    # headers = dict()
    # headers["x-oss-storage-class"] = "Standard"
    # headers["x-oss-object-acl"] = oss2.OBJECT_ACL_PRIVATE
    # 填写Object完整路径和字符串。Object完整路径中不能包含Bucket名称。
    # result = bucket.put_object('exampleobject.txt', 'Hello OSS', headers=headers)
    name = hashlib.md5(url.encode(encoding='utf-8')).hexdigest()
    print(name)
    result = bucket.put_object('novel/'+name+'.txt', content)

    # HTTP返回码。
    print('http status: {0}'.format(result.status))
    # 请求ID。请求ID是本次请求的唯一标识，强烈建议在程序日志中添加此参数。
    print('request_id: {0}'.format(result.request_id))
    # ETag是put_object方法返回值特有的属性，用于标识一个Object的内容。
    print('ETag: {0}'.format(result.etag))
    # HTTP响应头部。
    print('date: {0}'.format(result.headers['date']))

def url_content(url, proxies=False, i=0):
    print(url)
    time.sleep(random.randrange(6))
    if i > 5:
        return False
    try:
        response = requests.get(url, timeout=5, headers=DEFAULT_REQUEST_HEADERS)
    except:
        print('超时')
        return url_content(url, False, i + 1)
    list_txt = BeautifulSoup(response.text, 'html.parser')
    return list_txt


def postNovelMethod(value):
    result = requests.post(url='http://check.check.com/index/novel/detail', data=value)
    print(result.text)
    try:
        data = json.loads(result.text)
        print(data['data'])
        return data['data']
    except:
        print('错误')
        traceback.print_exc()


def getNovelMethod(value):
    result = requests.post(url='http://check.check.com/novel/default/search', data=value)
    print(result.text)
    try:
        data = json.loads(result.text)
        print(data['data'])
        return data
    except:
        print('错误')
        traceback.print_exc()


def postChapterMethod(value):
    result = requests.post(url='http://check.check.com/novel/chapter/index', data=value)
    print(result.text)
    try:
        data = json.loads(result.text)
        print(data)
    except:
        print('错误')
        traceback.print_exc()


def getContent(url, sort, novel):
    content = url_content(url)
    urls = content.find(class_='book-mulu').find_all('a')
    baseUrl = 'https://www.shicimingju.com'
    for url in urls:
        urlDetail = baseUrl + url.attrs['href']
        name = url.text.encode('iso-8859-1').decode('UTF-8')
        getDetail(urlDetail, sort, novel, name)
        sort = sort + 1


def getDetail(url, sort, novel, name=''):
    print(url)
    content = url_content(url)
    detail = content.find(class_='bookmark-list').text
    novel = {'novel': novel, 'sort': sort, 'name': name, 'content': detail, 'url': url}
    postChapterMethod(novel)


# novel = postNovelMethod({'title':'title','cate':'1','pic':'pic','author':'author','content':'content','url':'url'})

# postChapterMethod({'novel':novel,'sort':1,'name':'name','content':'content','url':'url'})
baseUrl = 'https://www.qxc11.com'
url = 'https://www.qxc11.com/chapter/'

def mainFun(n):
    listUrl = url + str(n+1)
    content = url_content(listUrl)
    
    if content is False:
        return False
    try:
        title = content.find('h1').text
    except:
        return False
    pic = content.find(class_='cover').find('img').attrs['src']
    author = content.find(class_='small').find_all('span')[0].text
    contents = content.find(class_='intro').find('dd').text
    urls = content.find(class_='listmain').find_all('dd')
    listAll = []
    for urlList in urls:
        urlSrc = baseUrl + urlList.find('a').attrs['href']
        detailContent = url_content(urlSrc)
        info = detailContent.find(id='chaptercontent').text
        ossUpload(urlSrc,info)
        #postNovelMethod({'url':urlSrc,'content':info})
mainFun(6)
exit() 


class myThread(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        print("开始线程：" + self.name)
        mainFun(self.delay)
        print("退出线程：" + self.name)


exitFlag = 0

for i in range(7590):
    n = i*3
    print('id=' + str(i))
    thread1 = myThread(1, "Thread-1", n)
    n = i*3 + 1
    thread2 = myThread(2, "Thread-2", n)
    n = i*3 + 2
    thread3 = myThread(2, "Thread-3", n)

    # 开启新线程
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    print("退出主线程,开始下一个循环")