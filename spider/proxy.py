# coding:utf-8
from bs4 import BeautifulSoup
import requests
import random
from _socket import timeout
from mysql import Mysql

import sys
from time import sleep
reload(sys)
sys.setdefaultencoding('utf8')

mysql = Mysql.db('server')

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        if tds[5].text == "HTTP":
#             print tds[1].text + ':' + tds[2].text
            ip_list.append(tds[1].text + ':' + tds[2].text)
    if not ip_list : 
        print 'web_data:' + web_data
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

def get_random_proxies():
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    return get_random_ip(ip_list)

### 没有参数则爬完整个分页，如果参数为1，则一直爬第1页
def run_by_dead(current_page = 1, page = None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    url = 'http://www.xicidaili.com/wt/' + str(current_page)
    print '=' * 50
    print '=' * 50
    print '=' * 50
    print '查询第 ' + str(current_page) + ' 页----------------- '
    print 'extract ---------------------------------- ' + url
    print '=' * 50
    print '=' * 50
    print '=' * 50
    ip_list = get_ip_list(url, headers=headers)
    print 'ip_list length ' + str(len(ip_list))
    for ip in ip_list:
        try :
            proxy_ip = 'http://' + ip
            print proxy_ip
            proxies = {'http': proxy_ip, 'https': proxy_ip}
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
    if page :
        current_page = current_page + 1
        if current_page > int(page) :
            return
    else :
        current_page = 1
    sleep_seconds = 60 * 5
    print 'sleep ' + str(sleep_seconds) + 's'
    sleep(sleep_seconds)
    run_by_dead(current_page = current_page, page = page)

if __name__ == '__main__':
    if len(sys.argv) == 1 :
        run_by_dead()
    else :
        run_by_dead(current_page = 1, page = int(sys.argv[1]))


