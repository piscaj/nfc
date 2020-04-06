#!/usr/bin/env python

import time
import json
import os
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
from mysql.connector import errorcode
import Adafruit_CharLCD as LCD
import tvCommand

#Load settings
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

#setup pi header pins for the 16x2 LCD display
lcd_rs        = 4  
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_columns   = 16  
lcd_rows      = 2
lcd_backlight = 4
#initialize lcd with settings above
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
lcd.message('Place Card to\npower on/off')

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
      lcd.message("Welcome\n" + result[1])
      cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
      db.commit()
      tvCommand.powerToggle() 
  else:
      lcd.message("Not authorized.")
    
      cursor.close()
      db.close()
  
  time.sleep(2)
  lcd.clear()
  lcd.message('Place Card to\npower on/off')
    
try:
  while True:
   
    id, text = reader.read()
    if id > 0:
      checkThisUser(id)
      print(id)
    
finally:
  GPIO.cleanup()