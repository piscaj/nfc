
import RPi.GPIO as GPIO
import time

class buzzerControl:
    
    def __init__(self,pin):  
        self._pin = pin
        GPIO.setup(self._pin,GPIO.OUT)
        
    
    def beep(self,i):
        for beeps in range(i):
            GPIO.output(self._pin,GPIO.HIGH)
            time.sleep(.1)
            GPIO.output(self._pin,GPIO.LOW)
            time.sleep(.1)