# coding=utf-8
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def send_by_content(mobiles, content):
    postData = { 'UserId' : '3047', 'Password' : 'HDjf_170901', 'Mobiles' : mobiles , 'Content' : content.encode('gbk')}
    #print postData
    r = requests.post("http://118.145.22.172:9888/smsservice/SendSMS", data=postData)
    print r.text

def send_by_msg(msg):
    postData = { 'UserId' : '3047', 'Password' : 'HDjf_170901', 'Msg' : msg.encode('gbk')}
    #print postData
    r = requests.post("http://118.145.22.172:9888/smsservice/SendSMS", data=postData)
    print r.text

def check_msg(msg):
    pass

if __name__ == '__main__' :
    test=False
    # 发送所有数据开关
    yes_all=False
    # 允许发送所有数据开关字符串
    yes_all_str='yes all'
    json = '"mobile":"{}","content":"{}"'
#     content = '尊敬的{}，送您5000减50、10000减100、20000减240和1.2%优惠券各1张，9月25日前有效。退订回TD'
#     content = '尊敬的{}，送您10000减100、30000减300、50000减600和1.2%优惠券各1张，9月25日前有效。退订回TD'
#     content = '尊敬的{}，送您10000减100、20000减200、30000减360和1.2%优惠券各1张，9月25日前有效。退订回TD'
#     content = '尊敬的{}，送您20000减200、30000减300、50000减600和1.2%优惠券各1张，9月25日前有效。退订回TD'
#     content = '尊敬的{}，您的发财节“特权收益项目”有效期仅剩最后12小时！还有{}万元可投资，6个月项目预期年化9.8%！退订回TD'
    content = '尊敬的{}，送您10000减200、20000减300、和1.5%优惠券各1张。27日前，用券投资，享国庆长假收益！退订回TD'
    if test :
        content += ' 测试'
        file = open("/Users/hyy/Downloads/ceshiduanxin.txt", 'r')
    else :
#         file = open("/Users/hyy/Downloads/发财节短信13415.txt", 'r')
#         file_path = "/Users/hyy/Documents/sms/20170921/A 6778.txt"
#         file_path = "/Users/hyy/Documents/sms/20170921/B 7856.txt"
#         file_path = "/Users/hyy/Documents/sms/20170921/C 4832.txt"
        #file_path = "/Users/hyy/Documents/sms/20170921/DEF 21214.txt"
#         file_path = "/Users/hyy/Documents/sms/20170922/发财节提醒短信 11492.txt"
        file_path = "/Users/hyy/Documents/sms/20170925/csv/1146_300000_00.csv"
        file = open(file_path, 'r')
        file_total_count = 0
        for line in open(file_path, 'r') :  
            file_total_count += 1
        file_name = file_path[file_path.rfind('/'):]
        print file_path
        print '文件总行数：', file_total_count
        if file_name.find(str(file_total_count)) == -1 :
            print '条数不对。'
            quit(0)
    # 批数据数
    batch_count = 200
    # 当前批存在多少条数据了
    count = 0
    # 总数据量
    total = 0
    # 过滤数据量
    skip = 29200
    # msg内容
    msg = '['
    # 逐行读取文件
    while True:
        line = file.readline()
        if not line:
            break
        if test : 
            line = str(line).replace('\n', '').replace('\r', '')
        else : 
            line = str(line).replace('\n', '').replace('\r', '')
        lines = line.split(',')
        # 获得第一个手机号码
        phone_number = str(lines[0])
        # 删除第一个元素，剩下的全是参数
        del lines[0]
        # 一行内容
        row_content = content
        # 循环直到没有{}占位符
        while row_content.index('{}') != -1 :
            # 循环参数数组
            for param in lines :
                # 替换占位符内容
                row_content = row_content.replace('{}', param, 1)
            # 参数循环完毕退出循环
            break
        # 转换成一行JSON记录
        row_json = json.format(phone_number, str(row_content))
        # 不是第一条则需要加分隔符
        if count != 0 :
            msg += ','
        # 拼接一个msg body
        msg += '{'
        msg += row_json
        msg += '}'
        count += 1
        total += 1
        # 过滤行数
        if total < skip :
            msg = '['
            count = 0
            continue
        if total == skip :
            msg = '['
            count = 0
            print '过滤 ' + str(total) + ' 行数据'
            continue
        # 输出前10条数据
        if count == 10 :
            print msg + ']'
        # 如果达到了一批数据量，则发送
        if count == batch_count :
            msg += ']'
#             print msg
            if yes_all :
                input_result = yes_all_str
            else :
                input_result = str(raw_input('确定执行吗？'))
            if yes_all == True or input_result == 'y' or input_result == yes_all_str :
                if input_result == yes_all_str :
                    yes_all = True
                print '发送 ' + str(count) + ' 条数据 ' + str(total)
                send_by_msg(msg)
            elif input_result == 'exit' or input_result == 'quit':
                print '退出程序'
                quit(0)
            else :
                print '取消执行'
            # 重新开始拼接和记录
            msg = '['
            count = 0
    # 结尾加]
    msg += ']'
    # 如果是最后一批数据，则发送
    if count != 0 :
        if count < 10 :
            print msg
#         print msg
        if yes_all :
            input_result = yes_all_str
        else :
            input_result = str(raw_input('确定执行吗？'))
        if yes_all == True or input_result == 'y' or input_result == yes_all_str :
            if input_result == yes_all_str :
                yes_all = True
            print '发送 ' + str(count) + ' 条数据 ' + str(total)
            send_by_msg(msg)
        elif input_result == 'exit' or input_result == 'quit':
            print '退出程序'
            quit(0)
        else :
            print '取消执行'
    print '================ 一共{}条数据'.format(str(total))


#     msg = '[{"mobile":"15618194808", "content":"是你啊111aaa"}　], {"mobile": "18637010312", "content":"是你啊222aaa"}]'
#     print msg
#     send_by_msg(msg)


