# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 21:42:31 2020

@author: litan
"""
import urllib
import gzip
from io import BytesIO

def gzdecode(data) :  
    compressedstream =  BytesIO(data)  
    gziper = gzip.GzipFile(fileobj=compressedstream)    
    data2 = gziper.read().decode("utf-8")  
    return data2

url ="https://www.icourse163.org/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc?csrfKey=f0f22d9fd41d4ab5aa90b2192bc35253"
headers = {"Host":" www.icourse163.org",
"Connection": "keep-alive",
"Content-Length": "53",
"User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
"Content-Type":" application/x-www-form-urlencoded",
"Accept": "*/*",
"Origin":"https://www.icourse163.org",
"Sec-Fetch-Site":"same-origin",
"Sec-Fetch-Mode": "cors",
"Referer": "https://www.icourse163.org/course/scnu-1205721821",
"Accept-Encoding": "gzip,deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Cookie":'''EDUWEBDEVICE=f51a2fd2e7da4c56a16d4940d567501b; hb_MA-A976-948FFA05E931_source=www.baidu.com; __yadk_uid=XvKVdDfz49iXXUdJBnGBi3QeyxBYN7Yd; WM_TID=Vlqm1ltwoFRERFUREAYqUlrCYJQOWu3o; NTESSTUDYSI=f0f22d9fd41d4ab5aa90b2192bc35253; utm="eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cHM6Ly93d3cuYmFpZHUuY29tL2xpbms/dXJsPUpDQlNhVEE0Q3h5d2toUG1wY1dRemtKbmtfVFYtT1JneFBOa19xTzBqU2tNM2YwTlF5a0NjM2xYcjIyazVCQXomd2Q9JmVxaWQ9YzA4ODBjY2IwMDJhMDgyYjAwMDAwMDA0NWU5NDU1N2E="; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1585803951,1586779523; WM_NI=6D2%2Fefgyc0jybyw1foMzjb5WdrrYaAOtPNFM3uNRdqfNxKqIt46DmeOge15QH5Y3SiBNJSfYMkAVzbg6%2BL6xC7dNpl3gIpZe%2FGlq42ByRSPbJsDNlnAj%2Bc0dXScumhmGMXk%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee85b45993b282b2b13af39e8ea2d85b978e9baef84baeb181adce61b0be9dd7fc2af0fea7c3b92af69cfed0e86ea5a7add1e973a2a7b9d2e5658fa6a683b85da8aebebae44b8daca0afc547f1ab82b3e77ba692b8acf443b8ecfaa5f06f8db9abd2b85b8ceb97d4d263829286b4e5538fb58fb7f96aa5eae5adb57481e9acaff368f1b98791d96fed99a492b73a82a79eb4d36a8aad8cafef6683b6e584b3709c8dad96f064af9983b9ea37e2a3; close_topBar=1; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1586779574''',
}


formdata ={
    "pageIndex":"4",
    "orderBy":"3",
    "pageSize":"20",
    "courseId":"1205721821",
        }
data = urllib.parse.urlencode(formdata).encode("utf-8")
request = urllib.request.Request(url,data = data,headers = headers)
res = urllib.request.urlopen(request).read()
print(gzdecode(res))