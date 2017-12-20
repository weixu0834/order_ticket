#coding:utf-8
import urllib
import urllib2
import collections
import time,threading

"""
用户信息，登录账号和密码
"""
mobile = "18408253663"
password = "Qq12345678"

"""
订单信息，包括挂号医生以及病人信息，姓名和身份证号码
"""
order_info = collections.OrderedDict()
order_info['nsId']= '1877'
order_info['nsName']= '张婉莹普通号'
order_info['nsPrice']= '10.00'
order_info['depaId']= '78'
order_info['depaName']= '(门)妇产科'
order_info['lockNo']= ''
order_info['hosId']= '769031850'
order_info['nsTime']= '2017-12-27'
order_info['nsPeriod']= '14:02-15:02'
order_info['nsDoctorseq']= '6002'
order_info['friendBirthday']= ''
order_info['gender']= '2'
order_info['urlsearch']= '?shopId=769031850&depaId=78&sourceId=1877&dateTime=2017-12-27&period=0&menuIndex=1'
order_info['patientCard']= ''
order_info['name']= "三月花"
order_info['age']= ''
order_info['sfcode']= '510401199512050124'
order_info['address']= ''
order_info['mobile']= '18408253663'
order_info['num']= ''
order_info['jhName']= ''
order_info['jhSfcode']= ''
order_info['jhMobile']= ''


cookies = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookies)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
}

def login():
    login_url = "http://www.ah12320.com/web/login"
    login_data = {'mobile': mobile, 'password': password}

    data = urllib.urlencode(login_data)
    request = urllib2.Request(login_url, data, headers)

    try:
        response = opener.open(request)
        result = eval(response.read().replace("null","\"\""))
        if(result['code'] == '1'):
            info = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'\n登录成功\n'
        else:
            info = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n登录失败\n'

        with open('log.txt', 'a') as f:
            f.write(info)

    except urllib2.HTTPError as e:
        print e.code


def order(period):
    data = urllib.urlencode(order_info)
    order_info['nsPeriod'] = period

    order = urllib2.Request(
            url = 'http://www.ah12320.com/web/order/add',
            headers = headers,
            data = data)

    try:
        response = opener.open(order)
        result = response.read()

        with open('log.txt', 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n' + period + ' ' + result + '\n')
    except urllib2.HTTPError as e:
        print e.code

    return result


def creat_period():
    period = []
    minute = 0

    #批量生成挂号时间段，8分钟为间隔，一般用于除周五外的挂号
    '''
    '''
    for hour in (8,9):
        while(((hour==8 or hour==14) and (minute+8<60)) or ((hour==9 or hour==15) and (minute<50))):
            period.append(
                str(hour).zfill(2) + ':' + str(minute).zfill(2) + '-' + str(hour).zfill(2) + ':' + str(
                    minute + 8).zfill(2))
            minute = minute+8
        if(hour==8):
            period.append(
                str(hour).zfill(2) + ':' + str(minute).zfill(2) + '-' + str(hour+1).zfill(2) + ':' + str(
                    minute + 8 - 60).zfill(2))
            minute = minute+8-60
	
	return period
'''
    for hour in (8,9):
        while(minute+8<60):
            period.append(
                str(hour).zfill(2) + ':' + str(minute).zfill(2) + '-' + str(hour).zfill(2) + ':' + str(
                    minute + 8).zfill(2))
            minute = minute+8

        period.append(
            str(hour).zfill(2) + ':' + str(minute).zfill(2) + '-' + str(hour+1).zfill(2) + ':' + str(
                minute + 8 - 60).zfill(2))
        minute = minute+8-60

    for hour in (14,15):
        for minute in range(0,60):
            if minute+8 > 60:
                period.append(
                    str(hour).zfill(2) + ':' + str(minute).zfill(2) + '-' + str(hour+1).zfill(2) + ':' + str(
                        minute + 8 - 60).zfill(2))
            else:
                period.append(
                    str(hour).zfill(2) + ':' + str(minute).zfill(2) + '-' + str(hour).zfill(2) + ':' + str(
                        minute + 8).zfill(2))
'''


def loop_order(period):
    flag = {'code': '1'}
    while(flag['code'] == '1'):
        key = order(period)
        print(period + ' ' + key)
        flag = eval(key)

if __name__ == '__main__':
    login()
    period = creat_period()

    threads = []
    for i in range(0,len(period)):
        t1 = threading.Thread(target=loop_order, args=(period[i],))
        threads.append(t1)

    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()