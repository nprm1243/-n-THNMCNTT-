# -*- coding: utf-8 -*-

import os
import dotenv
from dotenv import load_dotenv
from tkinter import Tk   
from tkinter.filedialog import askopenfilename, askdirectory
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

dotenv_file = dotenv.find_dotenv()
load_dotenv()
FILETOZIP = os.getenv('FILETOZIP')
ZIPFILE = os.getenv('ZIPFILE') # Sẽ lấy cùng tên với ZIPFILE, chỉ đổi đuôi
ZIPPATH = os.getenv('ZIPPATH') # Path mặc định của 7z, không cần setup lại (trừ khi thay đổi path cài đặt của 7z)
USERPATH = os.getenv('USERPATH') 
PASSWORDFILENAME = os.getenv('PASSWORDFILENAME')
DATASOURCE = os.getenv('DATASOURCE')
DIRTYDATAFILE = os.getenv('DIRTYDATAFILE')
CLEANDATAFILE = os.getenv('CLEANDATAFILE')
HOSTPATH = os.getenv('HOSTPATH')
CLIENTNAME = os.getenv('CLIENTNAME')

print("@fit.hcmus")
print("21KDL1_N2_THNMCNTT")
print("WELCOME TO MARKNICE CLIENT SETUP WIZARD")
print("")
print("Would you like to run setup wizard, the old data will be replaced [Y/N]:")
oke = input()
print(f'Your choice: {oke}')
while (oke != 'Y' and oke != 'N'):
    print("We only accept Y or N, please enter again:")
    oke = input()
    print(f'Your choice: {oke}')

if (oke == 'N'):
    exit(0)

Tk().withdraw()

print("Choose the folder where contain database/csv file for this project:")
USERPATH = askdirectory()
print(f"Folder you chose: {USERPATH}")

print("Choose dirty data file: ")
DIRTYDATAFILE = askopenfilename()
print(f"File you chose: {DIRTYDATAFILE[DIRTYDATAFILE.rfind('/')+1:]}")

print("Enter your clean data file name: ")
CLEANDATAFILE = input()
print(f"File you chose: {CLEANDATAFILE}")

print("Enter a name for your encypted file: ")
PASSWORDFILENAME = input()
print(f"Name you chose: {PASSWORDFILENAME}")

print("Enter host shared folder path: ")
HOSTPATH = input()
print(f"Path you chose: {HOSTPATH}")

print("Enter your client name: ")
CLIENTNAME = input()
print(f"Your client name: {CLIENTNAME}")

FILETOZIP = CLEANDATAFILE
DATASOURCE = USERPATH
os.environ['FILETOZIP'] = FILETOZIP
ZIPFILE = FILETOZIP
ZIPFILE = ZIPFILE[:ZIPFILE.find('.')] + '.zip'
os.environ['ZIPFILE'] = ZIPFILE
os.environ['USERPATH'] = USERPATH
os.environ['PASSWORDFILENAME'] = PASSWORDFILENAME
os.environ['DATASOURCE'] = DATASOURCE
os.environ['DIRTYDATAFILE'] = DIRTYDATAFILE[DIRTYDATAFILE.rfind('/')+1:]
os.environ['CLEANDATAFILE'] = CLEANDATAFILE
os.environ['HOSTPATH'] = HOSTPATH
os.environ['CLIENTNAME'] = CLIENTNAME

dotenv.set_key(dotenv_file, "FILETOZIP", os.environ["FILETOZIP"])
dotenv.set_key(dotenv_file, "ZIPFILE", os.environ["ZIPFILE"])
dotenv.set_key(dotenv_file, "USERPATH", os.environ["USERPATH"])
dotenv.set_key(dotenv_file, "PASSWORDFILENAME", os.environ["PASSWORDFILENAME"])
dotenv.set_key(dotenv_file, "DATASOURCE", os.environ["DATASOURCE"])
dotenv.set_key(dotenv_file, "CLIENTNAME", os.environ["CLIENTNAME"])
dotenv.set_key(dotenv_file, "DIRTYDATAFILE", os.environ["DIRTYDATAFILE"])
dotenv.set_key(dotenv_file, "CLEANDATAFILE", os.environ["CLEANDATAFILE"])
dotenv.set_key(dotenv_file, "HOSTPATH", os.environ["HOSTPATH"])

print("Setup done!")

print(f"Do you want to split data in {DIRTYDATAFILE} [Y/ N]?")
oke = input()
print(f'Your choice: {oke}')
while (oke != 'Y' and oke != 'N'):
    print("We only accept Y or N, please enter again:")
    oke = input()
    print(f'Your choice: {oke}')

if (oke == 'N'):
    exit(0)

print("How many parts will you divide the dataset into?")
part = int(input())
print(f"Choose your part in [1; {part}]:")
hihi = int(input())

print(f'Reading {DIRTYDATAFILE}...')
data = pd.read_csv(DIRTYDATAFILE)

data_splited = []
tmp = data.copy()
total_data = len(data)
for i in range(part-1):
    train_size = int(total_data/(part - i))
    test_size = total_data - train_size
    train_size = train_size/total_data
    test_size = test_size/total_data
    data_splited.append(0)
    data_splited[i], tmp = train_test_split(tmp, train_size = train_size, test_size= test_size)
    total_data = total_data - int(total_data/(part - i))
data_splited.append(tmp)

data_splited[hihi-1].to_csv('dirty.csv', index = False)