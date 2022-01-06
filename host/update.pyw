# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error
import rsa
import dotenv
from dotenv import load_dotenv
from rsa.pkcs1 import decrypt, encrypt
import zipfile
###########################################################################################################
#                                       LOAD ENVIROMENT VARIABLE
dotenv_file = dotenv.find_dotenv()
load_dotenv()
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
TRACKINGFILE = os.getenv('TRACKINGFILE')
CLIENTS = os.getenv('CLIENTS')
USERPATH = os.getenv('USERPATH')
SHAREFOLDER = os.getenv('SHAREFOLDER')
clients = CLIENTS.split(' ')
###########################################################################################################
#                                       SIGNAL PROCESSING
signal_file = open(TRACKINGFILE)
signal_data = signal_file.read()
signal_file.close()
signal_data = signal_data.split(' ')
signal = signal_data[0]
pass_file = signal_data[1]
###########################################################################################################
#                                         DECRYPTING
with open('private_key.key') as private_key_file:
    private_key = private_key_file.read()
private_key = rsa.PrivateKey.load_pkcs1(private_key, 'PEM')
with open(pass_file, 'rb') as file:
    file_to_decrypt = file.read()
decrypted_file = rsa.decrypt(file_to_decrypt, private_key).decode()
print(decrypted_file)
###########################################################################################################
#                                         UNZIP FILE
fantasy_zip = zipfile.ZipFile(f'{signal}.zip')
fantasy_zip.setpassword(str.encode(str(decrypted_file)))
fantasy_zip.extractall()
fantasy_zip.close()
###########################################################################################################
#                                         UPDATE DATABASE
dataset = pd.read_csv(f'{signal}.csv')
conn = mysql.connect(
    host = HOST,
    user = USER,
    password = PASSWORD
)

dataset = dataset.where(pd.notnull(dataset), '')
cursor = conn.cursor()
cursor.execute(f'DROP TABLE IF EXISTS marknice.{signal};')
cursor.execute(f'CREATE TABLE marknice.{signal} (Title MEDIUMTEXT,Author MEDIUMTEXT,Genre MEDIUMTEXT,SubGenre MEDIUMTEXT ,Height INT,Publisher MEDIUMTEXT)')
for i, row in dataset.iterrows():
    sql = f"INSERT INTO marknice.{signal} VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, tuple(row))
    conn.commit()

cursor = conn.cursor()
cursor.execute(f'DROP TABLE IF EXISTS marknice.host_data;')
cursor.execute(f'CREATE TABLE marknice.host_data (Title MEDIUMTEXT,Author MEDIUMTEXT,Genre MEDIUMTEXT,SubGenre MEDIUMTEXT ,Height INT,Publisher MEDIUMTEXT)')
query = ''
first = True
for client in clients:
    if (first == True):
        first = False
    else:
        query += ' UNION '
    query += f'SELECT * FROM marknice.{client}'
cursor.execute(query)
result = cursor.fetchall()
for item in result:
    sql = f"INSERT INTO marknice.host_data VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, tuple(item))
    conn.commit()
os.system('call notification.bat "database has been updated"')

###########################################################################################################
#                                         GENERATE NEW KEY
'''
(public_key, private_key) = rsa.newkeys(2048)
private_key_file = open("private_key.key", "w")
private_key_file.write(private_key.save_pkcs1().decode('utf-8'))
private_key_file.close()
public_key_file = open("public_key.key", "w")
public_key_file.write(public_key.save_pkcs1().decode("utf-8"))
public_key_file.close()
os.system(f'copy public_key.key "{SHAREFOLDER}"')
'''