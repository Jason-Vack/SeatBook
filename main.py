# -*- coding: UTF-8 -*-
import os  # 用于获得当前文件路径，满足移植性
import re
import time
# 控制访问
import urllib2
import requests
import cookielib
# 图像识别
import subprocess
from PIL import Image
# 邮件发送
import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText
import pstats
import cProfile
from contextlib import contextmanager


@contextmanager
def profiling(sortby='cumulative', limit=20):
    pr = cProfile.Profile()
    pr.enable()
    yield
    pr.disable()
    ps = pstats.Stats(pr).sort_stats(sortby)
    ps.print_stats(limit)


def mail():
    my_sender = 'conichi@foxmail.com'  # 发件人邮箱账号
    my_pass = 'oznkrmjckeyrebcb'  # 发件人邮箱密码
    msg = MIMEText('填写邮件内容', 'plain', 'utf-8')
    msg['From'] = formataddr(["Good morning", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(["Good morning", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = "预约成功"  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(my_sender, [my_user, ], msg.as_string())  # 对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接


# 识别png图片
def image_to_string():
    subprocess.check_call('C:\Python27\Tesseract-OCR\\tesseract.exe verify.png veristring -psm 7 digits', shell=True)
    with open('veristring.txt', 'r') as f:
        text = f.read().strip()  # 去除头尾的空格
    return text


# 获得验证码
def verify():
    while 1:
        url = 'http://zwyy.tsg.hrbeu.edu.cn/api.php/check'
        # 事实上，我并不清楚以下程序具体原理。。。
        filename = os.getcwd()+'\\cookie.txt'  # cookie保存位置
        cookie = cookielib.MozillaCookieJar(filename)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        initimage = opener.open(url)
        cookie.save(ignore_discard=True, ignore_expires=True)
        image = Image.open(initimage)
        image.save(os.getcwd()+'\\verify.png')  # 验证码图片保存位置
        # 识别verify.png为字符串veristring
        veristring = image_to_string()
        veristring = veristring.replace(" ", "")  # 去掉空格
        # 只有当识别为4个数字时停止循环并返回
        check = re.search('[0-9][]0-9][]0-9][0-9]', veristring)
        if check:
            return check.group(0)


# 登录与预约
def book(segment):
    imagestring = verify()
    loginurl = 'http://zwyy.tsg.hrbeu.edu.cn/api.php/login'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language ': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '51',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        "Host": "zwyy.tsg.hrbeu.edu.cn",
        'Origin': 'http: // zwyy.tsg.hrbeu.edu.cn',
        "Referer": "http://zwyy.tsg.hrbeu.edu.cn/Home/web/index/area/1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/59.0.3071.86 Safari/537.36",
        'X - Requested - With': 'XMLHttpRequest'
    }
    data = {
        'username': stuid,
        'password': password,
        'verify': imagestring
    }
    f = open(os.getcwd()+'\\cookie.txt')
    files = f.read()
    stringcookies = re.search('[A-Za-z0-9]{26}', files)  # 验证码的cookie为26位
    session = requests.session()  # 使用session保持连接
    cookies = dict(PHPSESSID=stringcookies.group(0))  # 手动添加cookie
    response = session.post(loginurl, headers=headers, data=data, cookies=cookies)
    # 若登录成功，就会返回数个cookie，通过检查返回值是否有某个cookie项就可以验证登录是否成功
    while response.cookies.get('expire', default=0) is 0:
        imagestring = verify()
        data = {
            'username': stuid,
            'password': password,
            'verify': imagestring
        }
        f = open(os.getcwd()+'\\cookie.txt')
        files = f.read()
        stringcookies = re.search('[A-Za-z0-9]{26}', files)
        session = requests.session()
        cookies = dict(PHPSESSID=stringcookies.group(0))
        response = session.post(loginurl, headers=headers, data=data, cookies=cookies)

    # 预约座位
    # 每秒刷新一次，直到5点
    bookeurl = 'http://zwyy.tsg.hrbeu.edu.cn/api.php/spaces/2'+seat+'/book'
    headers2 = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language ': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '84',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        "Host": "zwyy.tsg.hrbeu.edu.cn",
        'Origin': 'http: // zwyy.tsg.hrbeu.edu.cn',
        "Referer": "http://zwyy.tsg.hrbeu.edu.cn/Home/Web/area?area=22&segment=" + segment + "&day=2017-07-27"
                   "&startTime=07:00&endTime=22:00",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/59.0.3071.86 Safari/537.36",
        'X - Requested - With': 'XMLHttpRequest'
    }
    data2 = {
        'access_token': response.cookies.get('access_token'),
        'userid': stuid,
        'segment': segment,
        'type': '1'
    }
    cookies2 = dict(PHPSESSID=stringcookies.group(0), user_name=response.cookies.get('user_name'),
                    userid=response.cookies.get('userid'), expire=response.cookies.get('expire'),
                    access_token=response.cookies.get('access_token'))
    while re.search('05:00:0[5-9]', time.asctime(time.localtime(time.time()))) is None:
        time.sleep(1)
    print time.time()
    with profiling(sortby='tottime', limit=5):
        session.post(bookeurl, headers=headers2, data=data2, cookies=cookies2)
    print time.time()
    print 'the time of book is ' + time.asctime(time.localtime(time.time()))

    # 检查是否预约成功 ，未成功则发送邮件
    exam = session.get('http://zwyy.tsg.hrbeu.edu.cn/User/Index/book', cookies=cookies2)  # 个人中心url
    # 若当天预约成功，则会有形如“2017-08-11”字样
    day = time.localtime(time.time()).tm_mday + 6
    month = time.localtime(time.time()).tm_mon
    if day > change[str(month)]:
        day -= change[str(month)]
        month += 1
    if day < 10:
        if re.search(str(month) + '-0' + str(day), exam.text).group(0) is not None:
            mail()
    else:
        if re.search(str(month) + '-' + str(day), exam.text).group(0) is not None:
            mail()


# 用于控制预约程序的循环执行
def booktime():
    while 1:
        # 每小时检查一次，直到4点。re.search返回数组
        # time.asctime将把以秒为单位的time.time()转化为年月日格式字典的time.localtime()转换为字符串格式
        while re.search('04:[0-9]{2}:', time.asctime(time.localtime(time.time()))) is None:
            time.sleep(3600)
        # 获得当前时间的图书馆格式
        segment = str(46462+time.localtime(time.time()).tm_yday)
        # 如果早于4点28分，再等待半小时
        if time.localtime(time.time()).tm_min <= 28:
            time.sleep(1800)
        # 每分钟刷新一次，直到4：59
        while re.search('04:59:', time.asctime(time.localtime(time.time()))) is None:
            time.sleep(60)
        book(segment)


if __name__ == '__main__':
    stuid = '2014212127'
    password = '6SlgJ6PrNv'
    seat = '001'
    my_user = 'conichi@foxmail.com'  # 收件人邮箱账号

    print time.asctime(time.localtime(time.time()))
    # 每个月的天数，因为预约时间比当前系统时间提前6天，因此每个月末存在日期不规则变化情况；用于检查是否预约成功
    change = {'1': 31, '3': 31, '5': 31, '7': 31, '8': 31, '10': 31, '12': 31,
              '4': 30, '6': 30, '9': 30, '11': 30, '2': 28}
    booktime()
