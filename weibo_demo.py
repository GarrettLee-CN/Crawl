# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 16:08:41 2019

@author: GarrettLee-CN
"""

import requests
import urllib
import base64
import time
import re
import json
import rsa
import binascii
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from requests.packages.urllib3.connectionpool import InsecureRequestWarning
import random #随机函数

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
jsondata={}
#构造一个随机伪造报头
def header():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    UserAgent=random.choice(user_agent_list)

    header = {
        'User-Agent':UserAgent,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://weibo.com/?sudaref=www.baidu.com&display=0&retcode=6102',
        'Connection': 'keep-alive'
       }
    return header

header = header()#随机生成一个header

class Login(object):
    session = requests.session()
    user_name = "你的微博账号"  #微博账号
    pass_word = "你的微博密码"  #微博密码   
    def get_username(self):
        #request.su = sinaSSOEncoder.base64.encode(urlencode(username));
        return base64.b64encode(urllib.parse.quote(self.user_name).encode("utf-8")).decode("utf-8")
    
    def get_pre_login(self):
        #取servertime, nonce,pubkey
        #int(time.time() * 1000)
        params = {
                "entry":	"weibo",
            "callback":	"sinaSSOController.preloginCallBack",
            "su":	self.get_username(),
            "rsakt":	"mod",
            "checkpin":	"1",
            "client":	"ssologin.js(v1.4.19)",
            "_":	int(time.time() * 1000)
                }
        try:
            response = self.session.post("https://login.sina.com.cn/sso/prelogin.php", params = params, headers = header, verify = False)
            return json.loads(re.search(r"\((?P<data>.*)\)", response.text).group("data"))#转成json格式
        except:
            print("获取公钥失败")
            return 0
        
    def login(self):
        jsondata = self.get_pre_login()
        servertime = jsondata['servertime']
        print(servertime)
        nonce = jsondata['nonce']
        print(nonce)
        rsakv = jsondata['rsakv']
        print(rsakv)
        pubkey = jsondata['pubkey']
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        password_string = str(servertime) + '\t' + str(nonce) + '\n' + self.pass_word
        sp=binascii.b2a_hex(rsa.encrypt(password_string.encode("utf-8"), public_key)).decode("utf-8")
        post_data = {
                "entry":	"weibo",
                "gateway":	"1",
                "from":"",
                "savestate":	"7",
                "qrcode_flag":	"false",
                "useticket":	"1",
                "vsnf":	"1",
                "su":	self.get_username(),
                "service":	"miniblog",
                "servertime":servertime,
                "nonce":nonce,
                "pwencode":	"rsa2",
                "rsakv":rsakv,
                "sp":sp,
                "sr":	"1536*864",
                "encoding":	"UTF-8",
                "prelt":	"529",
                "url":	"https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
                "returntype":	"TEXT"
                }
        proxies = {
                'http': '129.28.66.50:80',
                  }
        login_data = self.session.post("https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)", data = post_data, headers = header, verify = False,proxies=proxies)
        
        print(login_data.json())
        params = {
                "ticket":login_data.json()['ticket'],
                "ssosavestate":	int(time.time()),
                "callback":	"sinaSSOController.doCrossDomainCallBack",
                "scriptId":	"ssoscript0",
                "client":	"ssologin.js(v1.4.19)",
                "_": int(time.time() * 1000)
                }
        self.session.post("https://passport.weibo.com/wbsso/login", params = params, verify = False, headers = header,proxies=proxies)
        return self.session

login = Login()
session = login.login()

print(session.cookies)
#以上均关于登录的一些信息

def get_data_session(userid, page):
    time.sleep(10)
    userid=userid
    page=page
    url="https://weibo.com/p/100505"+str(userid)+"/follow?relate=fans&page="+str(page)
    print(url)
    return session.post(url,verify = False, headers = header)

def get_data_res(userid,page):
    try:
        return get_data_session(userid,page)
    except:
        try:
            return get_data_session(userid,page)
        except:
            print("获取页码信息失败", userid,page)
            return 0

#由于微博的页面都是通过JS渲染的，因此我们需要对JS进行解析，找出其中含有html代码块的程序，并切分出来
def get_pure_json(json_draft):
    tag = '<script>FM.view'
    index = json_draft.find(tag)
    if index > -1:
        item = json_draft[index + len(tag) + 1:len(json_draft) - 1]
        if item[-1] == ')':
            item = item[:len(item) - 1]
        return item
    else:
        return None

#抓取粉丝列表的核心函数       
def get_data(userid,page):
    response = get_data_res(userid,page)
    data = list()
    if response:
        try:#和上述理由一样，我们需要对JS块进行切分，随后丢给get_pure_json函数进行一次预处理
            FansSplit_data = response.text.split("</script>")            
            json_str = {}
            for item in FansSplit_data:
                item = get_pure_json(item)

                if not item:
                    continue
                if item.find('"domid":"Pl_Official_HisRelation__49"') > -1:
                    json_str = item
                    
            json_data = json.loads(json_str)
            soup = BeautifulSoup(json_data['html'], 'lxml')            
            #6个方块
            infos = soup.findAll("li",{"class":"follow_item S_line2"})
            #print(len(infos)) 要是6就对了
            #print(infos)
            for info in infos:
                #昵称
                div_level = info.find("div",{"class":"info_name W_fb W_f14"})
                nick_name = (div_level.find("a",{"class":"S_txt1"}))
                data.append(nick_name.text)
                
                #用户ID
                user_ID=nick_name.get('usercard')[3:13]#这样做的目的是选取出固定长度的ID号
                data.append(user_ID)

                #性别
                gender=div_level.find("i")
                sex = gender.get('class')[1][5:]#sex.get('class')返回出来的结果是这样的['W_icon', 'icon_female']，所以用[1]取第二个值，随后再切片
                data.append(sex)

                #获取头像URL与下载头像，下载下来后，头像按照用户ID命名
                Icon = info.find("dt",{"class":"mod_pic"})
                pic = Icon.find("img")
                iconurl = pic.get('src')
                icon= requests.get(iconurl, timeout=3)
                dir = './images/' + user_ID + '.jpg'
                try:#存在有的头像没有的情况，为了不中断程序，我们需要做的就是设置一个try
                    fp = open(dir, 'wb')
                    fp.write(icon.content)
                    fp.close()
                except requests.exceptions.ConnectionError:
                    print('图片数据没有下载')
                data.append(iconurl) #将头像URL写下来
                
                #关注数
                div_follow=info.find("span",{"class":"conn_type"})
                followcount = div_follow.find("em").text
                data.append(followcount)
                
                #粉丝数与微博数
                div_fans_weibo = info.findAll("span",{"class":"conn_type W_vline S_line1"})
                for count in div_fans_weibo:
                    fans_weibocount = count.find("em").text
                    data.append(fans_weibocount)
                
                #关注方式
                div_from = info.find("div",{"class":"info_from"})
                fans_form=div_from.find("a").text
                data.append(fans_form)

            print(data)    
        except:pass
    return data


def save_data_to_csv(data):
    data = np.array(data).reshape(-1,8)
    result_weibo = pd.DataFrame(data)
    result_weibo.to_csv(data_file_name, mode = 'a', index = False, encoding = 'gb18030', header = False)
    
data_file_name = "./WEIBOID.csv"
column = pd.DataFrame({}, columns = ['昵称','ID',"性别","头像URL","关注数","粉丝数","微博数","关注方式"])
column.to_csv(data_file_name, index=False, encoding='gb18030') 

#此处由于批量加载学生信息进行数据获取工作并存储进EXCEL表中
df = pd.read_csv('stuID1.csv')
print(df)
for i in df["ID"]:
    for j in range(1,6):
        time.sleep(3)
        save_data_to_csv(get_data(i,j))