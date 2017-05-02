from bs4 import BeautifulSoup
import requests
import random
from _socket import timeout

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

def run_by_dead():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    url = 'http://www.xicidaili.com/nn/'
    ip_list = get_ip_list(url, headers=headers)
    for ip in ip_list:
        try :
            proxy_ip = 'http://' + ip
            print proxy_ip
            proxies = {'http': proxy_ip,'https': proxy_ip}
            url = 'http://ip.chinaz.com/getip.aspx'
            requests.adapters.DEFAULT_RETRIES = 5
            web_data = requests.get(url, headers=headers, proxies=proxies, timeout=5)
            print '=' * 50
            print web_data.text
            exit(0)
        except Exception , e:
            print e
    run_by_dead()

if __name__ == '__main__':
    #proxies = get_random_proxies()
#     proxies = {'http': 'http://58.101.16.133:8888'}
#     url = 'http://beijing.anjuke.com/community/?kw=%E6%81%92%E5%A4%A7'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
#     }
#     print(proxies)
#     web_data = requests.get(url, headers=headers, proxies=proxies, timeout=6000)
#     print web_data
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    
#     url = 'http://ip.chinaz.com/getip.aspx'
# #     url = 'http://beijing.anjuke.com/community/?kw=%E6%81%92%E5%A4%A7'
#     proxies = {'http': 'http://116.62.45.185:3128'}
#     while True:
#         try:
#             web_data = requests.get(url, headers=headers, proxies=proxies, timeout=5)
#             print '=' * 120
#             print web_data.text
#             exit(0)
#         except Exception, e:
#             print 'error'
    run_by_dead()
    
    
