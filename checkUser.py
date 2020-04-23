#!/usr/bin/env python3

import time
import json
import os
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
from mysql.connector import errorcode
from braviaTV import braviaTV
from lcd import lcdDisplay
from threading import Thread
from led import LedControl

#Load config
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__,"settings.json")) as settings:
    data = json.load(settings)

for settings in data["mySQLSettings"]:
    host  = settings.get("host")
    user = settings.get("user")
    password = settings.get("passwd")
    db = settings.get("database")

for settings in data["tvSettings"]:
    ip  = settings.get("ip")
    psk = settings.get("psk")
    mac = settings.get("mac")

mySQLcfg = {
    'host':host,
    'user':user,
    'passwd':password,
    'database':db
}

#create instance of the card reader
reader = SimpleMFRC522()
#create instance of the LCD
lcdDisplay = lcdDisplay()
#create instance of the Sony Bravia TV
tv = braviaTV(ip,psk,mac)
#create instance of the LED
light = LedControl()

lcdDisplay.message('Place card to\npower on/off')

def checkThisUser(id):
  stopWeather = Thread(target = light.stop)
  stopWeather.start()
  stopWeather.join()
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
      runway = Thread(target = light.rainbow)
      runway.start()
      lcdDisplay.clear()
      lcdDisplay.message("Welcome\n" + result[1])
      cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
      db.commit()
      tvPower = tv.powerToggle()
      lcdDisplay.clear()
      lcdDisplay.message("TV power state\n" + tvPower)
  else:
      lcdDisplay.message("Not authorized.")
      cursor.close()
      db.close()
      
  time.sleep(0.5)
  stopRunway = Thread(target = light.stop)
  stopRunway.start()
  runway.join()
  stopRunway.join()  
  lcdDisplay.clear()
  lcdDisplay.message('Place Card to\npower on/off')
  weather = Thread(target = light.showWeather)
  weather.start()

def readerStart():
  weather = Thread(target = light.showWeather)
  weather.start()
  #light.pulse(33,44,56)
  
  try:
    while True:
   
      id, text = reader.read()
      if id > 0:
        checkThisUser(id)
        print(id)
      
  finally:
    GPIO.cleanup()

if __name__ == '__main__':
    readerStart()
