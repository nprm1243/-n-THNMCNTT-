# -*- coding: utf-8 -*-

import os, datetime
from time import sleep
import dotenv
from dotenv import load_dotenv

dotenv_file = dotenv.find_dotenv()
load_dotenv()
FILETOZIP = os.getenv('FILETOZIP')
USERPATH = os.getenv('USERPATH')

filename = USERPATH + '/' + FILETOZIP
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
        #os.system('run.bat')
        print(tmp)
        os.system(f'call notification.bat "some change for {FILETOZIP} has been detected"')
        sleep(2)
        last_modification = modification_date(filename)
    sleep(1)