# coding:utf-8
import sys, os, re, urllib2

class JiuMa:

    def __init__(self) :
        self.h = 'http://web.9mli.com:8000/http.aspx?'
        self.h = 'http://api2.9mli.com/http.aspx?'
        #self.h = 'http://api.9mli.com/http.aspx?'
        self.code_path = os.getcwd()
        self.number_path = os.getcwd()
        self.code_url = 'https://www.hdfax.com/user/captcha'
        self.host_url = 'https://www.hdfax.com/snow/invitation/reward/156******08/8a81810f549988a501549f6118981010'
        self.user_name = 'blazerhe'
        self.pwd = 'hyy4646586'
        self.pid = '16694'
        self.jifen = ''
        self.money = ''
        self.tongshi = ''
        self.token = ''
        self.number = ''

    def login(self) :
        rst = urllib2.urlopen(self.h + 'action=loginIn&uid=%s&pwd=%s' % (self.user_name, self.pwd))
        rst = rst.read().split('|')
        self.token = rst[1]

        rst = urllib2.urlopen(self.h + 'action=getUserInfos&uid=%s&token=%s' % (self.user_name, self.token))
        rst = rst.read().split(';')
        self.jifen = rst[1]
        self.money = rst[2]
        self.tongshi = rst[3]

    def info(self) :
        print '用户名:' + self.user_name
        print '密钥:' + self.token
        print '积分:' + self.jifen
        print '余额:' + self.money
        print '可同时获取号码数:' + self.tongshi

    def get(self) :
        rst = urllib2.urlopen(self.h + 'action=getMobilenum&pid=%s&uid=%s&token=%s&size=1' % (self.pid, self.user_name, self.token))
        rst = rst.read()
        if rst == 'no_data' :
            print rst
            return
        self.number = rst.split('|')[0]
        outfile = open(self.number_path + '/last_number', 'w')
        outfile.write(self.number)
        outfile.close()
        print rst

    def release(self) :
        rst = urllib2.urlopen(self.h + 'action=ReleaseMobile&uid=%s&token=%s&mobile=%s' % (self.user_name, self.token, self.number))
        print rst.read()

    def code(self, number = None) :
        rst = urllib2.urlopen(self.h + 'action=getVcodeAndHoldMobilenum&uid=%s&token=%s&pid=%s&mobile=%s'%(self.user_name,self.token,self.pid,number))
        rst = rst.read()
        code = self.code_status(rst)
        if not number :
            number = self.number
        outfile = open(self.code_path + '/' + number, 'w')
        outfile.write(code)
        outfile.close()
        print code

    def code_status(self, s) :
        rst = None
        if s == 'not_receive' :
            rst = '还没有接收到验证码,请让程序等待几秒后再次尝试'
        elif len(s.split('|')) != 1 :
            rst = s.split('|')[1]
            re_str = '验证码(.*),'
            re_pat = re.compile(re_str)
            search_ret = re_pat.search(rst)
            if search_ret:
                rst = search_ret.groups()[0]
        else :
            rst = s
        return rst

if __name__ == '__main__' :
    jiuma = JiuMa()
    jiuma.login()

    if len(sys.argv) == 1 :
        jiuma.info()
        exit(0)

    param1 = sys.argv[1]
    if param1 == 'info' :
        jiuma.info()
        exit(0)
    elif param1 == 'get' :
        jiuma.get()
    elif param1 == 'release' :
        jiuma.release()
    elif param1 == 'code' :
        if len(sys.argv) == 3 :
            jiuma.code(number = sys.argv[2])
        else :
            print 'params length error.'
    jiuma.login()
    jiuma.info()


