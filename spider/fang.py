# coding=utf-8
import urllib
from pyquery import PyQuery as pyq
import sys
reload(sys)
sys.setdefaultencoding('utf8')

data_file = open('data_lianjia.csv', 'w+')

# 过滤存在的城市名称
unique_citys = []
def extract(url):
    http://sh.fang.lianjia.com/loupan/search恒大
    url = url.replace('anjuke.com', 'fang.anjuke.com/loupan/s?kw=' + urllib.quote('恒大'))
    print 'extract : ', url
    try :
        doc = pyq(url=url)
        cts = doc('.list-contents>.list-results>.key-list>.item-mod')
        city = doc(".city").text()
        if city in unique_citys :
            print 'city ' + city + ' 已经抓取过'
            return
        unique_citys.append(city)
        for i in cts:
            name = cts(i).find('.infos h3 .items-name').text().strip()
            html = cts(i).find(".favor-pos>.price").html()
            if html == None :
                html = cts(i).find(".favor-pos .around-price").html()
                price = ''
                unit = ''
                if html == None :
                    content = ''
                    referto_price = ''
                    referto_unit = ''
                else :
                    content = cts(i).find(".favor-pos .around-price").text().strip()
                    referto_price = cts(i).find(".favor-pos .around-price>span").text().strip()
                    referto_unit = html[html.index('</span>') + 7:].strip()
            else :
                price = cts(i).find(".favor-pos .price>span").text().strip()
                unit = html[html.index('</span>') + 7:].strip()
                content = cts(i).find(".favor-pos>.price").text().strip()
                referto_price = ''
                referto_unit = ''
            data_file.write(city + '\t' + name + '\t' + price + '\t' + unit + '\t' + content + '\t' + referto_price + '\t' + referto_unit+'\n')
            data_file.flush()
    except Exception, e:
        print e

file_object = open('url.csv')
i = 0
for line in file_object:
    print i
    url = line.replace('\n', '')
    extract(url)
    i = i + 1

#extract('http://beijing.anjuke.com')    
