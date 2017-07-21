# -*- coding: UTF-8 -*-
import re
import time
import urllib2
import requests
import cookielib
import subprocess
from PIL import Image


def image_to_string():
    subprocess.check_call('E:\Python\Tesseract-OCR\\tesseract.exe verify.png veristring -psm 7 digits', shell=True)
    with open('veristring.txt', 'r') as f:
        text = f.read().strip()
    return text


def verify():
    while 1:
        # 将验证码保存为本地图片verify.png
        url = 'http://zwyy.tsg.hrbeu.edu.cn/api.php/check'

        # 带cookie获得验证码图片
        filename = 'E:\Python\Files\SeatsAppointment\\cookie.txt'
        cookie = cookielib.MozillaCookieJar(filename)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        initimage = opener.open(url)
        cookie.save(ignore_discard=True, ignore_expires=True)
        image = Image.open(initimage)
        image.save('E:\Python\Files\SeatsAppointment\\verify.png')

        # 识别verify.png为字符串veristring
        veristring = image_to_string()
        veristring = veristring.replace(" ", "")
        check = re.search('[0-9][]0-9][]0-9][0-9]', veristring)
        if check:
            print check.group(0)
            return check.group(0)


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
        'username': '2014212127',
        'password': '6SlgJ6PrNv',
        'verify': imagestring
    }
    f = open('E:\Python\Files\SeatsAppointment\\cookie.txt')
    files = f.read()
    stringcookies = re.search('[A-Za-z0-9]{26}', files)
    session = requests.session()
    cookies = dict(PHPSESSID=stringcookies.group(0))
    response = session.post(loginurl, headers=headers, data=data, cookies=cookies)
    while response.cookies.get('expire', default=0) is 0:
        imagestring = verify()
        data = {
            'username': '2014212127',
            'password': '6SlgJ6PrNv',
            'verify': imagestring
        }
        f = open('E:\Python\Files\SeatsAppointment\\cookie.txt')
        files = f.read()
        stringcookies = re.search('[A-Za-z0-9]{26}', files)
        session = requests.session()
        cookies = dict(PHPSESSID=stringcookies.group(0))
        response = session.post(loginurl, headers=headers, data=data, cookies=cookies)

    # 预约座位
    bookeurl = 'http://zwyy.tsg.hrbeu.edu.cn/api.php/spaces/2030/book'
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
        "Referer": "http://zwyy.tsg.hrbeu.edu.cn/Home/Web/area?area=22&segment=" + segment + "&day=2017-07-26"
                   "&startTime=07:00&endTime=22:00",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/59.0.3071.86 Safari/537.36",
        'X - Requested - With': 'XMLHttpRequest'
    }
    data2 = {
        'access_token': response.cookies.get('access_token'),
        'userid': '2014212127',
        'segment': segment,
        'type': '1'
    }
    cookies2 = dict(PHPSESSID=stringcookies.group(0), user_name=response.cookies.get('user_name'),
                    userid=response.cookies.get('userid'), expire=response.cookies.get('expire'),
                    access_token=response.cookies.get('access_token'))
    session.post(bookeurl, headers=headers2, data=data2, cookies=cookies2)


def booktime():
    segment = '46663'
    has_done = 0
    check_re = '19:2[0-9]:'
    changetime = '19:3[0-9]:'
    while 1:
        while has_done is 0:
            time_now = re.search(check_re, time.asctime(time.localtime(time.time())))
            # while re.search('14:[0-9]{2}:', time.asctime(time.localtime(time.time()))) is None:
            #     time.sleep(3600)
            while time_now is None:
                time.sleep(60)
                print time.asctime(time.localtime(time.time()))
                time_now = re.search(check_re, time.asctime(time.localtime(time.time())))
            # 到5：30分后，执行登录以及预约操作
            book(segment)
            tosegment = int(segment)
            tosegment += 1
            segment = str(tosegment)
            has_done = 1
        while has_done is 1:
            time_now = re.search(changetime, time.asctime(time.localtime(time.time())))
            while time_now is None:
                time.sleep(300)
                print time.asctime(time.localtime(time.time()))
                time_now = re.search(changetime, time.asctime(time.localtime(time.time())))
            has_done = 0


if __name__ == '__main__':
    booktime()
