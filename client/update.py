# -*- coding: utf-8 -*-

import os
import rsa
import zipfile
import random, string
import dotenv
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from datetime import datetime
from rsa.pkcs1 import decrypt, encrypt
###########################################################################################################
#                                         LOAD ENVIROMENT VARIABLE
dotenv_file = dotenv.find_dotenv()
load_dotenv()
FILETOZIP = os.getenv('FILETOZIP')
ZIPFILE = os.getenv('ZIPFILE')
ZIPPATH = os.getenv('ZIPPATH')
USERPATH = os.getenv('USERPATH')
PASSWORDFILENAME = os.getenv('PASSWORDFILENAME')
DATASOURCE = os.getenv('DATASOURCE')
DIRTYDATAFILE = os.getenv('DIRTYDATAFILE')
CLEANDATAFILE = os.getenv('CLEANDATAFILE')
HOSTPATH = os.getenv('HOSTPATH')
CLIENTNAME = os.getenv('CLIENTNAME')
###########################################################################################################
#                                                  CLEAN DATA
path_host = r'{}/'.format(DATASOURCE)
with open(path_host+f'{DIRTYDATAFILE}') as f:
    data = pd.read_csv(f)
data.drop_duplicates()
clean_author = data["Title"]
clean_subgenre = data["SubGenre"]
for i in range(len(clean_author)):   
    if ', ' in str(clean_author[i]):
        index = str(clean_author[i]).index(",")
        if 'The' in str(clean_author[i]):
            clean_author[i] = 'The ' + clean_author[i][:index]
        if 'A' in str(clean_author[i]):
            clean_author[i] = 'A ' + clean_author[i][:index]
        if 'An' in str(clean_author[i]):
            clean_author[i] = 'An ' + clean_author[i][:index]
        if 'Foudation' in str(clean_author[i]):
            clean_author[i] = 'Foudation ' + clean_author[i][:index]
            
for i in range(len(clean_subgenre)):
    if '_' in str(clean_subgenre[i]):
        clean_subgenre[i] = str(clean_subgenre[i]).replace("_"," ",1)
        
data.to_csv(f'{CLEANDATAFILE}',index=False)
###########################################################################################################
#                                         DELETE OLD FILES
with open('dele.bat', 'w') as batch_file:
    batch_file.write(f"""@echo off
del {ZIPFILE} \{r'{}'.format(HOSTPATH)}
del {PASSWORDFILENAME} \{r'{}'.format(HOSTPATH)}""")
os.system('dele.bat')
###########################################################################################################
#                                         GENERATE PASSWORD
password = '';
dau = ['.', '^', '&', '$', '#', '@', ',', '`']
for i in range(31):
    tmp = random.randint(1, 2)
    if (tmp == 1):
        password += random.choice(string.ascii_letters)
    elif (tmp == 2):
        password += str(random.randint(0, 9))
    else:
        password += dau[random.randint(0, len(dau) - 1)]
###########################################################################################################
#                                         CREATE ZIP FILE
batchfile_data = f'''@ECHO OFF
set PATH=%PATH%;{ZIPPATH}
7z a {ZIPFILE} {FILETOZIP} -p{password}
'''
batchfile = open('compress.bat', 'w')
batchfile.write(batchfile_data)
batchfile.close()
os.startfile('compress.bat')
###########################################################################################################
#                                         ENCRYPT PASSWORD
with open('public_key.key') as public_key_file:
    public_key = public_key_file.read()
public_key = rsa.PublicKey.load_pkcs1(public_key, 'PEM')
encrypted_message = rsa.encrypt(str.encode(password), public_key)
encrypted_file = open(f'{PASSWORDFILENAME}', 'wb')
encrypted_file.write(encrypted_message)
encrypted_file.close()
###########################################################################################################
#                                         SEND FILE TO HOST
with open('signal.txt', 'w') as signal_file:
    signal_file.write(f'{CLIENTNAME} {PASSWORDFILENAME}')
with open('send.bat', 'w') as batch_file:
    batch_file.write(f"""@echo off
copy {ZIPFILE} \{r'{}'.format(HOSTPATH)}
copy {PASSWORDFILENAME} \{r'{}'.format(HOSTPATH)}
copy signal.txt \{r'{}'.format(HOSTPATH)}""")
os.system('send.bat')