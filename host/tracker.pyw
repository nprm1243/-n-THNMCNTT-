# -*- coding: utf-8 -*-

import os, datetime
from time import sleep
import dotenv
from dotenv import load_dotenv

dotenv_file = dotenv.find_dotenv()
load_dotenv()
TRACKINGFILE = os.getenv('TRACKINGFILE')

filename = TRACKINGFILE
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

last_modification = modification_date(filename)
print(last_modification)

while (1 == 1):
    tmp = modification_date(filename)
    if (tmp != last_modification):
        print(tmp, last_modification)
        last_modification = tmp
        os.system('wscript.exe invisible.vbs copy.bat')
        sleep(1)
        os.system('wscript.exe invisible.vbs update.bat')
        os.system('call notification.bat "A signal has been detected"')
        print(tmp)
        sleep(5)
        last_modification = modification_date(filename)
    sleep(1)