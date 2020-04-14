import colorsys
import time
from sys import exit
import numpy as np
import blinkt

    #blinkt.set_clear_on_exit()

class LedControl:
    
    def __init__(self):  
        self._running  = True 
        
    def stop(self):
        self._running = False
        #time.sleep(0.2)
        #blinkt.set_all(0, 0, 0)
        #blinkt.show()
        
        
    def setColor(self,color = [], *args):
        blinkt.set_all(0, 0, 0)
        blinkt.set_pixel(color)
        blinkt.show()
    
    def setAllColor(self,color = [], *args):
        blinkt.set_all(0, 0, 0)
        blinkt.set_all(color)
        blinkt.show()
            
    def runway(self):
        self._running = True
        while self._running:
            for i in range(8):
                blinkt.clear()
                blinkt.set_pixel(i, 255, 0, 0)
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
        #self._running = True
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

