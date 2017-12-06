# coding=utf-8
import urllib
import urllib2
import cookielib
import sys
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
    print 'begin~'
    url = 'https://s.lakala.com/rand.action?tempStr=0.8097082357853651'
    
#     image = Image.open('/Users/hyy/Downloads/rand.action.jpeg')
#     image.load()
#     vcode = pytesseract.image_to_string(image)
#     print str(vcode)
    import ssl
    context = ssl._create_unverified_context()       
    picture = urllib2.urlopen("https://s.lakala.com/rand.action?tempStr=1", context=context).read()
    local = open('yzm.jpeg', 'wb')
    local.write(picture)
    local.close()
    

