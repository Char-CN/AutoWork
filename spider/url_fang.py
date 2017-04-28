# coding=utf-8
import urllib
from pyquery import PyQuery as pyq
import sys
reload(sys)
sys.setdefaultencoding('utf8')

data_file = open('url_fang.csv', 'w+')

# 过滤存在的城市名称
unique_citys = []
def getUrls(url):
    try :
        doc = pyq(url=url)
        cts = doc('#senfe1 a')
        for i in cts:
            data_file.write(str(cts(i).attr('href')).strip() + '\n')
            data_file.flush()
    except Exception, e:
        print e

getUrls('http://fang.com/SoufunFamily.htm')
