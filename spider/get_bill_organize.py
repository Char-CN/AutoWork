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

def get_success_vcode(opener):
    picture = opener.open("https://bill.sand.com.cn/pages/verifyCode.jsp?flag=1499153731969").read()
    local = open('yzm_organize.jpeg', 'wb')
    local.write(picture)
    local.close()
    image = Image.open('yzm_organize.jpeg')
    image.load()
    vcode = pytesseract.image_to_string(image)
    if len(str(vcode)) != 4:
        print 'fail vcode : ', vcode
        return get_success_vcode(opener)
    postData = { 'verifyCode' : str(vcode) }
    request = urllib2.Request('https://bill.sand.com.cn/login!checkVerifyCode.action', urllib.urlencode(postData), headers)
    response = opener.open(request)
    result = response.read().decode('utf-8')
    if str(result).strip() != 'ok' :
        print 'fail vcode : ', vcode
        return get_success_vcode(opener)
    print 'success vcode : ', vcode
    return str(vcode)

def login(opener, username, password):
    vcode = get_success_vcode(opener)
    postData = { 'username' : username , 'password' : password , 'type':'3', 'loginType':'1', 'verifyCode' : vcode }
    request = urllib2.Request('https://bill.sand.com.cn/login.action', urllib.urlencode(postData), headers)
    response = opener.open(request)
    result = str(response.read()).strip()
    return result

def get_data(opener):
    try:
        response = opener.open("https://bill.sand.com.cn/showTransaction!getOrgList.action")
        response = response.read()
        data = json.loads(response)
        return data
    except Exception, e:
        print e
        return get_data(opener)

def data_to_file(data_file, data):
    for d in data:
        id = str(d['id']).strip().split('_')[0]
        organize_name = str(d['text']).strip()
        order_asc = str(d['id']).strip().split('_')[1]
        parent_id = str(d['parentId']).strip()
        row_str = id + '\t' + parent_id + '\t' + organize_name + '\t' + order_asc
        data_file.write(row_str + '\n')
        # 递归
        data_to_file(data_file, d['children'])

if __name__ == '__main__' :
    username = ''
    password = ''
    if len(sys.argv) == 1 :
        print 'Usage: python getdata.py ${username} ${password}'
        exit(-1)
    elif len(sys.argv) >= 3 :
        username = str(sys.argv[1])
        password = str(sys.argv[2])
    
    # 将cookies绑定到一个opener cookie由cookielib自动管理
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    login_result = login(opener, username=username, password=password)
    print 'login result : ', login_result
    if login_result != 'success' :
        print 'login fail ~~~~~'
        exit(-1)
    today = datetime.date.today()
    daykey = today.strftime("%Y%m%d")
    output_file_name = 'data/data_bill_organize_' + str(daykey) + '.csv'
    print output_file_name
    data_file = open(output_file_name, 'w+')
    data = get_data(opener)
    data_to_file(data_file, data)








