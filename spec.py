#! /usr/bin/python
#-*- coding: utf-8 -*-

from oled.serial import i2c, spi
from oled.device import sh1106, ssd1306
from oled.render import canvas
from oled.error import DeviceNotFoundError
import sys, Image
import subprocess
import time

# cava 실행
try:
    subprocess.check_output('pgrep -x cava', shell=True)
except:
    subprocess.call("cava &", shell=True)

# ssd1306 또는 sh1106 device 초기화
try:
    device = sh1106(i2c(port=1, address=0x3c))
except IOError:
    try:
        device = sh1106(spi(device=0, port=0))
    except DeviceNotFoundError as e:
        sys.stderr.write("ssd1306 or sd1106 not found: %s\n" % e)
        sys.exit(1)

# Audio Spectrum 표시
cava_fifo = open("/tmp/cava_fifo", 'r')
while True:
    data = cava_fifo.readline().strip().split(';')
    with canvas(device) as draw:
        for i in range(0,len(data)-1):
            try:
                draw.rectangle((i*3, 63, i*3+1, 63 - int(data[i])), outline='white', fill='white')
            except: pass
    time.sleep(0.05)
