#!\usr\bin\python
"""
Simulate the hands of a clock - Size matters
- Hours is 3 pixels, brightest in the middle pixel.
- Minutes is 1 pixels.
The seconds is the white pixel filling up the full strip one by one in the odd minute and turning off the white pixel in the even minute.
"""
from __future__ import print_function

from time import sleep
from datetime import datetime

import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

from NeopixelSim import NeopixelRing, hour_pixel

class Flood(object):

    def __init__(self, parent):

        self.np = NeopixelRing(parent, 200)
        self.time_now = datetime.now()
        self.time_then = self.time_now
        self.parent = parent
        
        self.display()
        self.parent.after(200, self.update)

    def display(self):
        for pixel in range(len(self.np.pixels)):
            self.np.set_pixel_color(pixel, 0, 0, 0, 0)

        brg = 250 if (self.time_now.minute % 2) == 0 else 0
        for idx in range(0, self.time_now.second+1):
            self.np.set_pixel_color(idx, 0, 0, brg, 0)

        brg = 0 if brg == 250 else 250
        for idx in range(self.time_now.second+1, 60):
            self.np.set_pixel_color(idx, 0, 0, brg, 0)

        r, g, b, w = self.np.get_pixel_color(hour_pixel(self.time_now.hour))
        self.np.set_pixel_color(hour_pixel(self.time_now.hour), 250, g, b, 0)
        r, g, b, w = self.np.get_pixel_color(self.time_now.minute)
        self.np.set_pixel_color(self.time_now.minute, g, 250, b, 0)


    def update(self):
        self.time_now = datetime.now()
        if self.time_now.second != self.time_then.second:
            brg = 250 if (self.time_now.minute % 2) == 0 else 0
            r, g, b, w = self.np.get_pixel_color(self.time_now.second)
            self.np.set_pixel_color(self.time_now.second, r, g, brg, w)
        
            if self.time_now.minute != self.time_then.minute:
                r, g, b, w = self.np.get_pixel_color(self.time_then.minute)
                self.np.set_pixel_color(self.time_then.minute, r, 0, b, w)
                r, g, b, w = self.np.get_pixel_color(self.time_now.minute)
                self.np.set_pixel_color(self.time_now.minute, r, 250, b, w)

            if self.time_now.hour != self.time_then.hour:
                r, g, b, w = self.np.get_pixel_color(hour_pixel(self.time_then.hour))
                self.np.set_pixel_color(hour_pixel(self.time_then.hour), 0, g, b, w)
                r, g, b, w = self.np.get_pixel_color(hour_pixel(self.time_now.hour))
                self.np.set_pixel_color(hour_pixel(self.time_now.hour), 250, g, b, w)

        self.time_then = self.time_now
        self.parent.after(200, self.update)
  
if __name__ == "__main__":
    ROOT = Tk()
    ROOT.title("Flood Clock")
    clock = Flood(ROOT)
    ROOT.mainloop()
