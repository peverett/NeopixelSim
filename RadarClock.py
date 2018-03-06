#!\usr\bin\python
"""
Hypno clock.

The white LED rotates once per second, lighting the Hour, Minute and Second 
as it passes. 

Colours fade quickly.
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

class Hypno(object):

    def __init__(self, parent):
        self.np = NeopixelRing(parent, 200)
        self.parent = parent
        self.time_now = datetime.now()
        self.time_then = self.time_now
        
        self.idx = 0
        self.display()
        self.parent.after(0, self.update)

    def display(self):
        self.time_now = datetime.now()

        for x in range(len(self.np.pixels)):
            self.np.set_pixel_color(x, 0, 0, 0, 0)

        for x in range(40,60,1):
            blue = 200 if x == self.time_now.second else 0
            green = 200 if x == self.time_now.minute else 0
            red = 200 if x == hour_pixel(self.time_now.hour) else 0

            white = (x-40) * 10
            self.np.set_pixel_color(x, red, green, blue, white)

    def update(self):
        if self.idx == 0:
            self.time_now = datetime.now()
            
        blue = 250 if self.idx == self.time_now.second else 0
        green = 250 if self.idx == self.time_now.minute else 0
        red = 250 if self.idx == hour_pixel(self.time_now.hour) else 0
        
        self.np.set_pixel_color(self.idx, red, green, blue, 200)

        prev = self.idx
        for x in range(20):
            prev = prev-1 if prev > 0 else 59
            r, g, b, w = self.np.get_pixel_color(prev)
            r = r - 10 if r else 0
            g = g - 10 if g else 0
            b = b - 10 if b else 0
            w = w - 10 if w else 0
            self.np.set_pixel_color(prev, r, g, b, w)

        self.idx = self.idx + 1 if self.idx < 59 else 0

        # 60 LED doesn't divide evenly into 1000ms (== 1 s) so delay size
        # is 17, 17, 16 (repeat 20 times = 1000).
        delay = 16 if (self.idx % 3) == 0 else 17
        self.parent.after(delay, self.update)

if __name__ == "__main__":
    ROOT = Tk()
    ROOT.title("Hypno Clock")
    clock = Hypno(ROOT)
    ROOT.mainloop()
