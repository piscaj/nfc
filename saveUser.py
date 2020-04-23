#!/usr/bin/env python3

import time 
#raspberry Pie GPIO library
import RPi.GPIO as GPIO
#card reader library
from mfrc522 import SimpleMFRC522
#database reader
import mysql.connector
#LCD panel library for 16x2 display
import Adafruit_CharLCD as LCD

#Load config
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__,"settings.json")) as settings:
    data = json.load(settings)

for settings in data["mySQLSettings"]:
    host  = settings.get("host")
    user = settings.get("user")
    password = settings.get("passwd")
    db = settings.get("database")

mySQLcfg = {
    'host':host,
    'user':user,
    'passwd':password,
    'database':db
}

db = mysql.connector.connect(**mySQLcfg)
#make connection to database

#create object to execute operations on the database
cursor = db.cursor()

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

try:
    while True:
        
        lcd.clear()
        message = '.......'
        lcd.message(message)
        for i in range(lcd_columns-len(message)):
            time.sleep(0.1)
            lcd.move_right()
        for i in range(lcd_columns-len(message)):
            time.sleep(0.1)
            lcd.move_left()
        lcd.clear()
        message = 'Ready...\nPlace new card'
        lcd.message(message)
            
        id, text = reader.read()
        cursor.execute("SELECT id FROM users WHERE rfid_uid="+str(id))
        cursor.fetchone()

        if cursor.rowcount >= 1:
            lcd.clear()
            lcd.message("Overwrite\nexisting user?")
            overwrite = input("Overwite (Y/N)? ")
            if overwrite[0] == 'Y' or overwrite[0] == 'y':
                lcd.clear()
                lcd.message("Overwriting user.")
                time.sleep(1)
                sql_insert = "UPDATE users SET name = %s WHERE rfid_uid=%s"
            else:
                continue
        else:
            sql_insert = "INSERT INTO users (name, rfid_uid) VALUES (%s, %s)"
        lcd.clear()
        lcd.message('Enter new name')
        new_name = input("Name: ")

        cursor.execute(sql_insert, (new_name, id))

        db.commit()

        lcd.clear()
        lcd.message("User " + new_name + "\nSaved")
        time.sleep(2)
finally:
    GPIO.cleanup()
