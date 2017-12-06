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

    image = Image.open('yzm.jpeg')
    image.load()
    vcode = pytesseract.image_to_string(image)
    
    print str(vcode)
    
    