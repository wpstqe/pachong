# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re
from bs4 import BeautifulSoup
import requests

brower = webdriver.Chrome(r"F:\python\yhai\chromedriver.exe")
for i in range(160):
    print("https://appmarket.1hai.cn/Article?id="+str(i+1))
    brower.get("https://appmarket.1hai.cn/Article?id="+str(i+1))
    wait = WebDriverWait(brower, 3)
    time.sleep(3)
    content = brower.find_element_by_id('root').get_attribute('innerHTML')
    try:
        title = brower.find_element_by_xpath('//div[@class="comm-block"]/h3/strong')
        filename = 'article/'+str(i)+title+'.html'
        with open(filename,'w',encoding='gb18030', errors='ignore') as file_object:
            file_object.write(str(content))
    except:
        filename = 'article/'+str(i)+'.html'
        with open(filename,'w',encoding='gb18030', errors='ignore') as file_object:
            file_object.write(str(content))
        continue
    finally:
        print("final print")
    print(title)

    

