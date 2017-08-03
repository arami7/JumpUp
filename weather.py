#!/usr/bin/python
#-*- coding: utf-8 -*-

from oled.serial import i2c, spi
from oled.device import sh1106, ssd1306
from oled.render import canvas

import os, sys, time
from PIL import ImageFont

from mpd import MPDClient, MPDError, CommandError

import datetime
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

os.environ["LC_COLLATE"] = "ko_KR.UTF-8"

#---------------------------------------------------------------------

weather = {}

now = datetime.datetime.now()
hour = str('%02d' % now.hour) + '00'
ymd = str(now.year) + str('%02d' % now.month) + str('%02d' % now.day)
#DsmX = 67
#DsmY = 101

weatherUrl = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib?ServiceKey='
serviceKey = 'kVqkqCYGqRzYue8Q11m0xTQkcmFQK9%2BeZSuuTPmBmzWIUBFjAp8FZiWs0I756NpjelmA6ch6i4Jo0FgHxa%2BGjA%3D%3D'

url = weatherUrl + serviceKey + '&base_date=' + ymd + '&base_time=' + hour + '&nx=67' + '&ny=101' + '&_type=json'

r = requests.get(url)

print(r)

weather['resultCode'] = int(r.json()['response']['header']['resultCode'])
if (weather['resultCode'] != 0):
    sys.stderr.write("Weather forecast Response: %s\n" % r.json()['response']['header']['resultMsg'])


tmp = {}
for data in r.json()['response']['body']['items']['item']:
    tmp[data['category']] = data['obsrValue']

tem = str(tmp['T1H'])
humidity = str(tmp['REH'])

print(u'온도: ' + tem) 
print(u'습도: ' + humidity)

print_tem = '온도: ' + tem + 'C'
print_hum = '습도: ' + humidity + '%'

#---------------------------------------------------------------

gulim14 = ImageFont.truetype('/home/pi/fonts/NGULIM.TTF', 12)



def main():

    while True:
        # print raw_disp_mode
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        nowDay = now.strftime('%a')
        nowTime = now.strftime('%p %I:%M')
        # print(nowDate + '  ' + nowTime)

        with canvas(device) as draw:
            draw.text((0, 0), unicode(nowDate), font=gulim14, fill='white')
            draw.text((100, 0), unicode(nowDay), font=gulim14, fill='white')
            draw.text((0,16), unicode(nowTime), font=gulim14, fill='white')

            draw.text((0, 32), unicode(print_tem), font=gulim14, fill='white')
            draw.text((0, 48), unicode(print_hum), font=gulim14, fill='white')
        time.sleep(1)



if __name__ == "__main__":
    try:
        device = sh1106(i2c(port=1, address=0x3c))
    except IOError:
        try:
            device = sh1106(spi(device=0, port=0))
        except IOError:
            sys.exit(1)

    main()









