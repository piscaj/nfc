import colorsys
import time
from sys import exit
import numpy as np
import blinkt
import requests

    #blinkt.set_clear_on_exit()

class LedControl:
    
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

    API_KEY = '7cb3cebc17d4311f4be0b58c3af8e06d'
    CITY_ID = '4929055'

    url = 'http://api.openweathermap.org/data/2.5/weather'

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

    def draw_thermo(self,temp):
        v = temp
        v /= 40
        v += (1 / 8)
        self.show_graph(v, 255, 0, 0)

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
        


