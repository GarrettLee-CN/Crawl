# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:00:37 2020

@author: Administrator
"""
from urllib import parse
import time

#URL中文编码问题
keyword=['教育技术学','教育学','药理学','计算机科学','生物学']
urlkw = '''http://www.gaoxiaojob.com/plus/search.php?keyword='''
urlpg='''&PageNo='''
for kw in keyword:
    
    kw=parse.quote_plus(kw)
    #parse.unquote_plus(url)解码
    for page in range(1,10):
        time.sleep(3)
        urlrsarch = urlkw+kw+urlpg+str(page)
        print("当前抓取的页码是："+urlrsarch)

        