#!/usr/bin/env python

import time 
#raspberry Pie GPIO library
import RPi.GPIO as GPIO
#card reader library
from mfrc522 import SimpleMFRC522
#database reader
import mysql.connector
#LCD panel library for 16x2 display
import Adafruit_CharLCD as LCD

#make connection to database
db = mysql.connector.connect(
    host="localhost",
    user="attendanceadmin",
    passwd="scoobydoo",
    database="attendancesystem"

#create object to execute operations on the database
cursor = db.cursor()

#create object for the card reader
reader = SimpleMFRC522()

#setup for LCD panel
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

try:
  while True:
    lcd.clear()
    lcd.message('Place Card to\nrecord attendance')
    id, text = reader.read()

    cursor.execute("Select id, name FROM users WHERE rfid_uid="+str(id))
    result = cursor.fetchone()

    lcd.clear()

    if cursor.rowcount >= 1:
      lcd.message("Welcome " + result[1])
      cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
      db.commit()
    else:
      lcd.message("User does not exist.")
    time.sleep(2)
finally:
  GPIO.cleanup()