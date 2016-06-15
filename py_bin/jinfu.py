# coding:utf-8

import os, urllib2, urllib, cookielib, gzip, StringIO, base64, json

code_path = os.getcwd()
webcode_url = 'https://www.hdfax.com/user/captcha'
inviteCode = '8a81810f549988a501549f6118981010'
host_url = 'https://www.hdfax.com/snow/invitation/reward/156******08/8a81810f549988a501549f6118981010'

class JinFu() :
    
    def __init__(self) :
        self.urlopener = None
        self.phone_number = ''
        self.captchaToken = ''
        self.webcode = ''
        self.smscode = ''
        self.kek = ''
        self.tpk = ''

    def login(self) :
        cookiejar = cookielib.CookieJar()
        urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        urllib2.install_opener(urlopener)
        
        urlopener.addheaders.append(('Accept', 'application/json, text/javascript, */*; q=0.01'))
        urlopener.addheaders.append(('Accept-Encoding', 'gzip'))
        urlopener.addheaders.append(('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6'))
        urlopener.addheaders.append(('Connection', 'keep-alive'))
        urlopener.addheaders.append(('Content-Length', '0'))
        urlopener.addheaders.append(('Host', 'www.hdfax.com'))
        urlopener.addheaders.append(('Origin', 'www.hdfax.com'))
        urlopener.addheaders.append(('Referer', host_url))
        urlopener.addheaders.append(('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'))
        urlopener.addheaders.append(('X-Requested-With', 'XMLHttpRequest'))
        self.urlopener = urlopener

    def get_webcode(self) :
        urlcontent = self.urlopener.open(urllib2.Request(webcode_url, urllib.urlencode({ })))
        urlcontent = gzip.GzipFile(fileobj=StringIO.StringIO(urlcontent.read()), mode="r")
        ret_dict = json.loads(urlcontent.read())
        print code_path
        outfile = open(code_path + '/code.jpg', 'w')
        outfile.write(base64.b64decode(ret_dict["applyPicCaptchaResponse"]["captcha"]))
        outfile.close()
        self.captchaToken = ret_dict["applyPicCaptchaResponse"]["captchaToken"]
        print self.captchaToken

    def input_phone_number(self) :
        phone_number = raw_input('Please enter the phone_number:')
        self.phone_number = phone_number
        print phone_number

    def input_webcode(self) :
        webcode = raw_input('Please enter the webcode:')
        self.webcode = webcode
        print webcode

    def send_smscode(self) :
        params = { 'phoneNumber' : self.phone_number, 'captchaToken' : self.captchaToken, 'captchaCode' : self.webcode }
        urlcontent = self.urlopener.open(urllib2.Request('https://www.hdfax.com/user/mobile/sms', urllib.urlencode(params)))
        print urlcontent.read()

    def input_smscode(self) :
        smscode = raw_input('Please enter the smscode:')
        self.smscode = smscode
        print smscode

    def register(self) :
        try :
            urlcontent = self.urlopener.open(urllib2.Request('https://www.hdfax.com/encryption/getTpSecurityKeys', urllib.urlencode({ })))
            ret_dict = json.loads(urlcontent.read())
            self.kek = ret_dict['kek']
            self.tpk = ret_dict['tpk']
            print self.kek
            print self.tpk
            params = { 'phoneNumber' : self.phone_number,
                      'smsCode' : self.smscode, 
                      'marketChannel' : 'promotion',
                      'inviteCode' : inviteCode,
                      'kek' : self.kek,
                      'tpk' : self.tpk }
            urlcontent = self.urlopener.open(urllib2.Request('https://www.hdfax.com/user/register', urllib.urlencode(params)))
            print urlcontent.read()
            urlcontent = gzip.GzipFile(fileobj=StringIO.StringIO(urlcontent.read()), mode="r")
            print urlcontent
            print urlcontent.read()
        except Exception, e:
            print e
            return False
        return True
        
if __name__ == '__main__' :
    jinfu = JinFu()
    jinfu.login()
    jinfu.get_webcode()
    jinfu.input_phone_number()
    jinfu.input_webcode()
    jinfu.send_smscode()
    jinfu.input_smscode()
    while True : 
        rst = jinfu.register()
        print rst
        if rst == True :
            break
    print 'done!'
