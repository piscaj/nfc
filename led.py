import colorsys
import time
from sys import exit
import numpy as np
import blinkt
import requests

    #blinkt.set_clear_on_exit()

class LedControl:
    
    #Settings for weather
    API_KEY = '7cb3cebc17d4311f4be0b58c3af8e06d'
    CITY_ID = '4929055'
    url = 'http://api.openweathermap.org/data/2.5/weather'
    
    def __init__(self):  
        self._running  = True 
        self._temp = 0
        
    #This is used to kill processes
    def stop(self):
        self._running = False 
        
    def setColor(self,pix,r,g,b):
        blinkt.set_pixel(pix,r,g,b)
        blinkt.show()
    
    def setAllColor(self,pix,r,g,b):
        blinkt.set_all(pix,r,g,b)
        blinkt.show()
            
    def runway(self):
        blinkt.set_all(0, 0, 0)
        blinkt.show()
        self._running = True
        blinkt.set_pixel(4,255,255,0)
        blinkt.show()
        blinkt.set_pixel(4,0,0,0)
        blinkt.show()
        blinkt.set_pixel(3,255,255,0)
        blinkt.show()
        blinkt.set_pixel(3,0,0,0)
        blinkt.show()
        blinkt.set_pixel(2,255,255,0)
        blinkt.show()
        blinkt.set_pixel(2,0,0,0)
        blinkt.show()
        time.sleep(0.04)
        while self._running:
            for i in range(8):
                blinkt.clear()
                blinkt.set_pixel(i, 119, 255, 0)
                blinkt.show()
                blinkt.time.sleep(0.05)
        print("Runway LED thread ended...")
        blinkt.set_all(0, 0, 0)
        blinkt.show()
    
    def make_gaussian(self,fwhm):
        x = np.arange(0, blinkt.NUM_PIXELS, 1, float)
        y = x[:, np.newaxis]
        x0, y0 = 3.5, 3.5
        fwhm = fwhm
        gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
        return gauss

    def flash(self):
        blinkt.set_all(0, 0, 0)
        blinkt.show()
        self._running = True
        while self._running:
            
            for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
                fwhm = 5.0 / z
                gauss = self.make_gaussian(fwhm)
                start = time.time()
                y = 4

                for x in range(blinkt.NUM_PIXELS):
                    h = 0.5
                    s = 1.0
                    v = gauss[x, y]
                    rgb = colorsys.hsv_to_rgb(h, s, v)
                    r, g, b = [int(255.0 * i) for i in rgb]
                    blinkt.set_pixel(x, r, g, b)

                blinkt.show()
                end = time.time()
                t = end - start

                if t < 0.04:
                    time.sleep(0.04 - t)
        print("Flash LED thread ended...")
        blinkt.set_all(0, 0, 0)
        blinkt.show()
        

    def update_weather(self):
        payload = {
            'id': self.CITY_ID,
            'units': 'metric',
            'appid': self.API_KEY
     }
        try:
            r = requests.get(url=self.url, params=payload)
            self._temp = r.json().get('main').get('temp')
            print('Temperture = ' + str(self._temp) + ' C')

        except requests.exceptions.ConnectionError:
            print('Connection Error')

    def show_graph(self,v, r, g, b):
        v *= blinkt.NUM_PIXELS
        for x in range(blinkt.NUM_PIXELS):
            if v < 0:
                r, g, b = 0, 0, 0
            else:
                r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
            blinkt.set_pixel(x, r, g, b)
            v -= 1
        blinkt.show()

    def pulse(self):
        step = 0
        while self._running:
            if step == 0:
                blinkt.set_all(128, 0, 0)

            if step == 1:
                blinkt.set_all(0, 128, 0)

            if step == 2:
                blinkt.set_all(0, 0, 128)

            step += 1
            step %= 3
            blinkt.show()
            time.sleep(0.5)

    def draw_thermo(self,temp):
        v = temp
        temp = float(temp)
        if 35.6 <= temp <= 37.7:
            r = 255 
            g = 0
            b = 0
        if 33.9 <= temp <= 35.5:
            r = 255 
            g = 131
            b = 58
        if 32.2 <= temp <= 33.80:
            r = 255 
            g = 164
            b = 58
        if 31.1 <= temp <= 32.10:
            r = 255 
            g = 184
            b = 58
        if 29.4 <= temp <= 31:
            r = 222 
            g = 210
            b = 58    
        if 27.7 <= temp <= 29.3:
            r = 255 
            g = 236
            b = 58            
        if 26.1 <= temp <= 27.6:
            r = 255 
            g = 249
            b = 58            
        if 24.4 <= temp <= 26:
            r = 249 
            g = 255
            b = 58     
        if 22.7 <= temp <= 24.3:
            r = 236
            g = 255
            b = 58
        if 21.1 <= temp <= 22.6:
            r = 210
            g = 255
            b = 58    
        if 18.8 <= temp <= 21:
            r = 177
            g = 255
            b = 58    
        if 17.2 <= temp <= 18.7:
            r = 111
            g = 255
            b = 58     
        if 15.5 <= temp <= 17.1:
            r = 58
            g = 255
            b = 98
        if 13.8 <= temp <= 15.4:
            r = 58
            g = 255
            b = 190
        if 12.2 <= temp <= 13.7:
            r = 58
            g = 255
            b = 210
        if 11.1 <= temp <= 12.1:
            r = 58
            g = 255
            b = 236
        if 9.4 <= temp <= 11:
            r = 58
            g = 255
            b = 255
        if 7.7 <= temp <= 9.3:
            r = 58
            g = 236
            b = 255
        if 4.4 <= temp <= 7.6:
            r = 58
            g = 210
            b = 255
        if 3.3 <= temp <= 4.3:
            r = 58
            g = 177
            b = 255
        if 0.5 <= temp <= 3.2:
            r = 58
            g = 124
            b = 255                     
        if -2.7 <= temp <= 0.5:
            r = 58
            g = 65
            b = 255            
        if -6.6 <= temp <= -2.6:
            r = 104
            g = 58
            b = 255      
        if -7.7 <= temp <= -6.5:
            r = 157
            g = 58
            b = 255
        if -12.2 <= temp <= -7.6:
            r = 216
            g = 58
            b = 255
        if -15 <= temp <= -12.1:
            r = 255
            g = 58
            b = 249
        if temp < -14:
            r = 255
            g = 58
            b = 210
               
        v /= 40
        v += (1 / 8)
        self.show_graph(v, r, g, b)

    def showWeather(self):
        blinkt.set_all(0, 0, 0)
        blinkt.show()
        self._running = True
        while self._running:
            self.update_weather()
            self.draw_thermo(self._temp)
            time.sleep(120)
        print("Weather LED thread ended...")
        blinkt.set_all(0, 0, 0)
        blinkt.show()
        
    def rainbow(self):
        spacing = 360.0 / 16.0
        hue = 0
        blinkt.set_brightness(0.1)
        
        blinkt.set_all(0, 0, 0)
        blinkt.show()
        self._running = True
        blinkt.set_pixel(4,255,255,0)
        blinkt.show()
        blinkt.set_pixel(4,0,0,0)
        blinkt.show()
        blinkt.set_pixel(3,255,255,0)
        blinkt.show()
        blinkt.set_pixel(3,0,0,0)
        blinkt.show()
        blinkt.set_pixel(2,255,255,0)
        blinkt.show()
        blinkt.set_pixel(2,0,0,0)
        blinkt.show()
        time.sleep(0.04)
        
        while self._running:
            hue = int(time.time() * 1000) % 360
            for x in range(8):
                offset = x * spacing
                h = ((hue + offset) % 360) / 360.0
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
                blinkt.set_pixel(x, r, g, b)
            blinkt.show()
            time.sleep(0.001)
        print("Rainbow LED thread ended...")
        blinkt.set_all(0, 0, 0)
        blinkt.show()

