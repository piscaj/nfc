import colorsys
import time
from sys import exit
import numpy as np
import blinkt
import requests
import random
import json
from threading import Thread


class weatherAlert:
    
    def __init__(self):  
        self._running  = True 
    
    def stop(self):
        self._running = False
        print("Trying to terminate Alert!") 
    
    def alert(self,x,r,g,b,level):
        self._running  = True 
        while self._running:
            _x = x
            __r, __g, __b = r, g, b
            _r, _g, _b = __r, __g, __b
            
            if level == 1:
             for i in range(20):
               if self._running:
                 _r,_g,_b = self.darken_color(_r,_g,_b)
                 time.sleep(.01)
                 for i in range(_x):
                     blinkt.set_pixel(i, _r, _g, _b)
                 blinkt.show()
               else:
                 print("Weather Alert thread ended...") 
                 break
             for i in range(60):
               if self._running:
                 _r,_g,_b = self.lighten_color(_r,_g,_b)
                 if _r >= __r: r = __r
                 else: r = _r
                 if _g >= __g: g = __g
                 else: g = _g
                 if _b >= __b: b = __b
                 else: b = _b
                 if (r == __r) and (g == __g) and (b == __b) and (self._running):
                     for i in range(_x):
                         blinkt.set_pixel(i, r, g, b)
                     blinkt.show()
                     print("Color temp updated!!!")
                     break
                 else:
                     time.sleep(.01)
                     for i in range(_x):
                         blinkt.set_pixel(i, r, g, b)
                     blinkt.show()
               else: 
                 print("Weather Alert thread ended...") 
                 break
             time.sleep(5)
            
            if level == 2:
             for i in range(15):
               if self._running:
                 _r,_g,_b = self.darken_color(_r,_g,_b)
                 #time.sleep(.01)
                 for i in range(_x):
                     blinkt.set_pixel(i, _r, _g, _b)
                 blinkt.show()
               else:
                 print("Weather Alert thread ended...") 
                 break
             for i in range(60):
               if self._running:
                 _r,_g,_b = self.lighten_color(_r,_g,_b)
                 if _r >= __r: r = __r
                 else: r = _r
                 if _g >= __g: g = __g
                 else: g = _g
                 if _b >= __b: b = __b
                 else: b = _b
                 if (r == __r) and (g == __g) and (b == __b) and (self._running):
                     for i in range(_x):
                         blinkt.set_pixel(i, r, g, b)
                     blinkt.show()
                     print("Color temp updated!!!")
                     break
                 else:
                     #time.sleep(.01)
                     for i in range(_x):
                         blinkt.set_pixel(i, r, g, b)
                     blinkt.show()
               else: 
                 print("Weather Alert thread ended...") 
                 break
             time.sleep(.5)
             
        print("Weather Alert thread ended...")
    
    def adjust_color_lightness(self,r, g, b, factor):
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        l = max(min(l * factor, 1.0), 0.0)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)
    
    def lighten_color(self,r, g, b, factor=0.1):
        return self.adjust_color_lightness(r, g, b, 1 + factor)
    
    def darken_color(self,r, g, b, factor=0.1):
        return self.adjust_color_lightness(r, g, b, 1 - factor)
       
class LedControl:
    
    def __init__(self,apiKey,cityID):  
        self._running  = True 
        self._temp = 0
        self._condition = "Clear"
        self._apiKey = apiKey
        self._cityID = cityID
        self._weatherAlert = False
        self.R = 0
        self.G = 0
        self.B = 0
        self.X = 0
    
    #Weather data location
    url = 'http://api.openweathermap.org/data/2.5/weather'
        
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
            'id': self._cityID,
            'units': 'metric',
            'appid': self._apiKey
     }
        try:
            r = requests.get(url=self.url, params=payload)
            data = r.json()
            self._temp = data.get('main').get('temp')
            for result in data.get('weather'):
                self. _condition = result.get("id")
            print('Temperture = ' + str(self._temp) + ' C' + " Conditions = " + str(self._condition))

        except requests.exceptions.ConnectionError:
            print('Connection Error')

    def show_graph(self,v, r, g, b):
        v *= blinkt.NUM_PIXELS
        pixCount = 0
        print("Weather alert: ",self._weatherAlert)
        for x in range(blinkt.NUM_PIXELS):
            if v < 0:
                r, g, b = 0, 0, 0
            else:
                _r, _g, _b = r, g, b
                r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
                pixCount = pixCount +1
            blinkt.set_pixel(x, r, g, b)
            v -= 1
        _x = pixCount
        __r, __g, __b = _r, _g, _b
        if self._weatherAlert:
            self.X = _x
            self.R = __r
            self.G = __g
            self.B = __b
            return self._weatherAlert
        else:
            for i in range(15):
                 if self._running:
                    _r,_g,_b = self.darken_color(_r,_g,_b)
                    time.sleep(.01)
                    for i in range(_x):
                        blinkt.set_pixel(i, _r, _g, _b)
                    blinkt.show()
            for i in range(60):
                 if self._running:
                    _r,_g,_b = self.lighten_color(_r,_g,_b)
                    if _r >= __r: r = __r
                    else: r = _r
                    if _g >= __g: g = __g
                    else: g = _g
                    if _b >= __b: b = __b
                    else: b = _b
                    if (r == __r) and (g == __g) and (b == __b):
                        for i in range(_x):
                            blinkt.set_pixel(i, r, g, b)
                        blinkt.show()
                        print("Color temp updated!!!")
                        break
                    else:
                        time.sleep(.01)
                        for i in range(_x):
                            blinkt.set_pixel(i, r, g, b)
                        blinkt.show()
        
    def adjust_color_lightness(self,r, g, b, factor):
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        l = max(min(l * factor, 1.0), 0.0)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)
    
    def lighten_color(self,r, g, b, factor=0.1):
        return self.adjust_color_lightness(r, g, b, 1 + factor)
    
    def darken_color(self,r, g, b, factor=0.1):
        return self.adjust_color_lightness(r, g, b, 1 - factor)

    def pulse(self,r,g,b):
        
        for i in range(4):
            r,g,b = self.lighten_color(r,g,b)
            time.sleep(1)
        for i in range(4):
            self.darken_color(r,g,b)
            time.sleep(1)

    def draw_thermo(self,temp):
        listOkConditions  =      [800,801,802,803,804]
        listBadConditions =      [200,201,210,211,230,231,
                                  300,301,310,311,313,321,
                                  500,501,520,521,600,601,
                                  611,612,613,615,620,612,
                                  701,721]
        listExtremeConditions =  [202,212,221,232,302,312,
                                  314,502,503,504,511,522,
                                  531,602,616,622,711,741,
                                  751,731,762,771,781]
        v = temp
        temp = float(temp)
        if 35.51 <= temp <= 37.80:
            r = 255 
            g = 0
            b = 0
        if 33.81 <= temp <= 35.50:
            r = 255 
            g = 131
            b = 58
        if 32.11 <= temp <= 33.80:
            r = 255 
            g = 164
            b = 58
        if 31.01 <= temp <= 32.10:
            r = 255 
            g = 184
            b = 58
        if 29.31 <= temp <= 31.00:
            r = 222 
            g = 210
            b = 58    
        if 27.61 <= temp <= 29.30:
            r = 255 
            g = 236
            b = 58            
        if 26.01 <= temp <= 27.60:
            r = 255 
            g = 249
            b = 58            
        if 24.31 <= temp <= 26.00:
            r = 249 
            g = 255
            b = 58     
        if 22.61 <= temp <= 24.30:
            r = 236
            g = 255
            b = 58
        if 21.01 <= temp <= 22.60:
            r = 210
            g = 255
            b = 58    
        if 18.71 <= temp <= 21.00:
            r = 177
            g = 255
            b = 58    
        if 17.11 <= temp <= 18.70:
            r = 111
            g = 255
            b = 58     
        if 15.41 <= temp <= 17.10:
            r = 58
            g = 255
            b = 98
        if 13.71 <= temp <= 15.40:
            r = 58
            g = 255
            b = 190
        if 12.11 <= temp <= 13.70:
            r = 58
            g = 255
            b = 210
        if 11.01 <= temp <= 12.10:
            r = 58
            g = 255
            b = 236
        if 9.31 <= temp <= 11.00:
            r = 58
            g = 255
            b = 255
        if 7.61 <= temp <= 9.30:
            r = 58
            g = 236
            b = 255
        if 4.31 <= temp <= 7.60:
            r = 58
            g = 210
            b = 255
        if 3.21 <= temp <= 4.30:
            r = 58
            g = 177
            b = 255
        if 0.51 <= temp <= 3.20:
            r = 58
            g = 124
            b = 255                     
        if -2.61 <= temp <= 0.50:
            r = 58
            g = 65
            b = 255            
        if -6.51 <= temp <= -2.60:
            r = 104
            g = 58
            b = 255      
        if -7.61 <= temp <= -6.50:
            r = 157
            g = 58
            b = 255
        if -12.11 <= temp <= -7.60:
            r = 216
            g = 58
            b = 255
        if -15.00 <= temp <= -12.10:
            r = 255
            g = 58
            b = 249
        if temp < -14.99:
            r = 255
            g = 58
            b = 210
        if self._condition in listOkConditions:
            self._weatherAlert = 0    
        if self._condition in listBadConditions:
            self._weatherAlert = 1
        if self._condition in listExtremeConditions:
            self._weatherAlert = 2   
        v /= 40
        v += (1 / 8)
        alert = self.show_graph(v, r, g, b)
        return alert

    def showWeather(self): 
        blinkt.set_all(0, 0, 0)
        blinkt.show()
        self._running = True
        while self._running:
            self.update_weather()
            alert = self.draw_thermo(self._temp)
            if alert:
                print("We have a weather alert. Threat level = ",alert)
                weatherAlert = Thread(target = a.alert, args = (self.X,self.R,self.G,self.B,alert))
                weatherAlert.start()
            else:
                print("No weather alert. Threat level = ",alert)
            for i in range(120):
                if self._running:
                    time.sleep(1)
            if alert:
                weatherAlertStop = Thread(target = a.stop)
                weatherAlertStop.start()
                weatherAlert.join()
                weatherAlertStop.join()
        if alert:
            weatherAlertStop = Thread(target = a.stop)
            weatherAlertStop.start()
            weatherAlert.join()
            weatherAlertStop.join()
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

a = weatherAlert()