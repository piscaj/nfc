#!/usr/bin/env python3

import time
import json
import os
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
from mysql.connector import errorcode
import tvCommand
from lcd import lcdDisplay

#Load config
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__,"settings.json")) as settings:
    data = json.load(settings)

for settings in data["mySQLSettings"]:
    HOST  = settings.get("host")
    USER = settings.get("user")
    PASS = settings.get("passwd")
    DB = settings.get("database")

mySQLcfg = {
    'host':HOST,
    'user':USER,
    'passwd':PASS,
    'database':DB
}

#create object for the card reader
reader = SimpleMFRC522()

lcdDisplay = lcdDisplay()

lcdDisplay.message('Place card to\npower on/off')

def checkThisUser(id):
  try:
    db = mysql.connector.connect(**mySQLcfg)
    
  except mysql.connector.Error as err:
   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
   elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
   else:
      print(err)
   
  else:  
      cursor = db.cursor()
      cursor.execute("Select id, name FROM users WHERE rfid_uid="+str(id))
      result = cursor.fetchone()
  
  if cursor.rowcount >= 1:
      lcdDisplay.clear()
      lcdDisplay.message("Welcome\n" + result[1])
      cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
      db.commit()
      tvCommand.powerToggle() 
  else:
      lcdDisplay.message("Not authorized.")
    
      cursor.close()
      db.close()
  
  time.sleep(1)
  lcdDisplay.clear()
  lcdDisplay.message('Place Card to\npower on/off')
    
try:
  while True:
   
    id, text = reader.read()
    if id > 0:
      checkThisUser(id)
      print(id)
    
finally:
  GPIO.cleanup()