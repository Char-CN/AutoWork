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
    local = open('yzm_pos_details.jpeg', 'wb')
    local.write(picture)
    local.close()
    image = Image.open('yzm_pos_details.jpeg')
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

def get_data_by_page(opener, formdata, error_count):
    if error_count >= 20:
        print 'error count >= 20, please check it .'
        return None
    try:
        response = opener.open("https://bill.sand.com.cn/searchTransaction.action", urllib.urlencode(formdata))
        response = response.read()
        data = json.loads(response)
        return data
    except Exception, e:
        print e
        error_count += 1
        return get_data_by_page(opener, formdata, error_count)

if __name__ == '__main__' :
    username = ''
    password = ''
    if len(sys.argv) == 1 :
        print 'Usage: python getdata.py ${username} ${password} [${begin_date}] [${end_date}]'
        exit(-1)
    elif len(sys.argv) >= 3 :
        username = str(sys.argv[1])
        password = str(sys.argv[2])
    begin_date = ''
    end_date = ''
    if len(sys.argv) > 4 :
        begin_date = str(sys.argv[3])
        end_date = str(sys.argv[4])
    elif len(sys.argv) > 3 :
        begin_date = str(sys.argv[3])
        end_date = str(sys.argv[3])
    else :
        begin_date = str(datetime.date.today() - datetime.timedelta(days=1))
        end_date = begin_date
    
    begin = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    # 将cookies绑定到一个opener cookie由cookielib自动管理
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    login_result = login(opener, username=username, password=password)
    print 'login result : ', login_result
    if login_result != 'success' :
        print 'login fail ~~~~~'
        exit(-1)
    
    start = begin
    delta = datetime.timedelta(days=1)
    print 'begin time', begin.strftime("%Y-%m-%d")
    print 'end time', end.strftime("%Y-%m-%d")
    while start <= end:
        daykey = start.strftime("%Y%m%d")
        output_file_name = 'data/data_pos_details_' + daykey + '.csv'
        print 'output_file_name : ', output_file_name
        data_file = open(output_file_name, 'w+')
        current_page = 1
        total = None
        count = 0
        while total == None or current_page <= total:
            formdata = {
                'beginDate' : '',
                'endDate' : '',
                'currentPage':str(current_page),
                'merCode':'',
                'accBeginDate':start.strftime("%Y-%m-%d"),
                'accEndDate':start.strftime("%Y-%m-%d"),
                'cardType':'0',
                'tmlCode':'',
                'txnType':'0',
                'acqCode':'0',
            }
            print 'request form data ', formdata
            data = get_data_by_page(opener, formdata, 0)
            if data == None :
                break
            if total == None :
                total = int(data['pager']['lastPage'])
                print 'total page : ', total
                if total == 0 :
                    print 'no data, break ...'
                    break
            for row in data['data'] :
                row_str = str(row['merCode']).strip()\
                + '\t' + str(row['tmlCode']).strip()\
                + '\t' + str(row['organizationName']).strip()\
                + '\t' + str(row['cardType']).strip()\
                + '\t' + str(row['dcTypeId']).strip()\
                + '\t' + str(row['cardId']).strip()\
                + '\t' + str(row['acqCodeName']).strip()\
                + '\t' + str(row['txnTypeName']).strip()\
                + '\t' + str(row['txnDate']).strip()\
                + '\t' + str(row['txnTime']).strip()\
                + '\t' + str(row['accDate']).strip()\
                + '\t' + str(row['txnAmt']).strip().replace(",", "")\
                + '\t' + str(row['txnAccountAmt']).strip().replace(",", "")\
                + '\t' + str(row['txnFee']).strip().replace(",", "")\
                + '\t' + str(row['systemNo']).strip()
                if debug and current_page == 1 :
                    print row_str
                data_file.write(row_str + '\n')
                data_file.flush()
                count += 1
            current_page += 1
        print start.strftime("%Y-%m-%d") + ' data total count : ', count
        start += delta
