# coding=utf-8
import urllib
import urllib2
import cookielib
import pytesseract
import json
from PIL import Image
from cookielib import CookieJar
from pyquery import PyQuery as pyq
from time import sleep

from bs4 import BeautifulSoup
import requests
import random
import datetime

import sys
from ensurepip import __main__
reload(sys)
sys.setdefaultencoding('utf8')

debug = False

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
}

if __name__ == '__main__' :
    username = ''
    password = ''
    config_id = ''
    if len(sys.argv) == 1 :
        print 'Usage: python getdata.py ${username} ${password} [${begin_date}] [${end_date}]'
        exit(-1)
    elif len(sys.argv) >= 4 :
        username = str(sys.argv[1])
        password = str(sys.argv[2])
        config_id = str(sys.argv[3])
    params = { }
    if len(sys.argv) > 3:
        count = 0
        for i in sys.argv:
            if count < 3:
                count += 1
                continue
            strs = str(i).split("=")
            if len(strs) == 2 :
                params[strs[0]] = strs[1]
    params['config_id'] = config_id
    print params
    # 将cookies绑定到一个opener cookie由cookielib自动管理
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    postData = { 'userName' : username , 'password' : password }
    request = urllib2.Request('http://us.xiwanglife.com/userservice/login.do', urllib.urlencode(postData), headers)
    response = opener.open(request)
    print response.read()
#     postData = { 'config_id' : '212' , 'aaa' : 'asd222方案' }
    request = urllib2.Request('http://ds.idc.xiwanglife.com/view/addTask.do', urllib.urlencode(params), headers)
    response = opener.open(request)
    print response.read()




