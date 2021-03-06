#!/usr/bin/env python
import Adafruit_CharLCD as piLCD
import time 

class lcdDisplay:
    
    lcd_rs        = 4  
    lcd_en        = 6  #Altered to add BLINKT 24 to 6
    lcd_d4        = 5  #Altered to add BLINKT 23 to 5
    lcd_d5        = 17
    lcd_d6        = 18 
    lcd_d7        = 22
    lcd_columns   = 16  
    lcd_rows      = 2
    lcd_backlight = 4
    
    lcd = piLCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
    
    def message(self, text):
        self.lcd.message(text)
   
    def clear(self):
        self.lcd.clear()
    
   
    