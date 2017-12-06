# coding:utf-8
from bs4 import BeautifulSoup
import requests
import random
from _socket import timeout
from mysql import Mysql

import sys
reload(sys)
sys.setdefaultencoding('utf8')

mysql = Mysql.db('server')

### 没有参数则爬完整个分页，如果参数为1，则一直爬第1页
def run_by_dead():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    rst = mysql.select('select * from proxy_ip')
    for row in rst:
        try :
            ip = str(row[0]) + ':' + str(row[1])
            proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
            requests.adapters.DEFAULT_RETRIES = 5
            response = requests.get('http://ip.chinaz.com/getip.aspx', headers=headers, proxies=proxies, timeout=5)
            print '=' * 50
            content = str(response.text).strip()
            print content
            # {ip:'119.5.1.53',address:'四川省南充市 联通'} 
            if content.startswith('{') and content.endswith('}') :
                content = str(content[1:len(content) - 1]).strip()
                print content
                contents = content.split(',')
                if len(contents) == 2 :
                    real_ip = str(contents[0].split(':')[1]).strip()
                    address = str(contents[1].split(':')[1]).strip()
                    address = str(address[1:len(address) - 1]).strip()
                    if real_ip.startswith("'") and real_ip.endswith("'") :
                        real_ip = str(real_ip[1:len(real_ip) - 1]).strip()
                        ips = ip.split(':')
                        print '*' * 50
                        print real_ip
                        print ips[0]
                        print '*' * 50
                        if real_ip == ips[0] :
                            print 'ip success... insert database'
                            sql = """
                            insert into proxy_ip(ip, port, type, website, address, enable) values ('{ip}','{port}','{type}','{website}','{address}','{enable}')
                            ON DUPLICATE KEY UPDATE ip='{ip}',port='{port}',type='{type}',website='{website}',address='{address}',enable='{enable}'
                            """.format(ip=real_ip, port=ips[1], type='HTTP', website=url, address=address, enable='1')
                            mysql.insert(sql)
                        else :
                            print 'ERROR: parse error4... 测试IP代理未成功'
                    else :
                        print 'ERROR: parse error3... 结果解析格式不正确'
                else :
                    print 'ERROR: parse error2... 结果解析个数不正确'
            else :
                print 'ERROR: parse error1... 网页返回不正确'
            print '=' * 50
        except Exception , e:
            print str(Exception)
            print str(e)

if __name__ == '__main__':
    run_by_dead()


