#!\usr\bin\python
"""
Display hours, minutes and seconds with trails of fading pixels, like a 
comet tale.
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

def inc_pix(idx):
    return 0 if idx == 59 else idx+1

def dec_pix(idx):
    return 59 if idx == 0 else idx-1

class Comet(object):

    def __init__(self, parent):
        self.np = NeopixelRing(parent, 200)
        self.parent = parent
        self.time_now = datetime.now()
        self.time_then = self.time_now
        
        self.display()
        self.parent.after(200, self.update)

    def display(self):
        self.time_now = datetime.now()
        for x in range(len(self.np.pixels)):
            self.np.set_pixel_color(x, 0, 0, 0, 0)

        idx = self.time_now.second
        blue = 240
        for x in range(16):
            self.np.set_pixel_color(idx, 0, 0, blue, 0)
            blue -= 16
            idx = dec_pix(idx)

        idx = self.time_now.minute
        green = 240
        for x in range(16):
            r, g, b, w = self.np.get_pixel_color(idx)
            self.np.set_pixel_color(idx, r, green, b, w)
            green -= 16
            idx = dec_pix(idx)

        idx = hour_pixel(self.time_now.hour)
        red = 240
        for x in range(16):
            r, g, b, w = self.np.get_pixel_color(idx)
            self.np.set_pixel_color(idx, red, g, b, w)
            red -= 16
            idx = dec_pix(idx)

        self.time_then = self.time_now

    def update(self):
        self.time_now = datetime.now()

        if (self.time_now.second != self.time_then.second):
            idx = self.time_now.second
            blue = 240
            for x in range(16):
                r, g, b, w = self.np.get_pixel_color(idx)
                self.np.set_pixel_color(idx, r, g, blue, w)
                blue -= 16
                idx = dec_pix(idx)

        if (self.time_now.minute != self.time_then.minute):
            idx = self.time_now.minute
            green = 240
            for x in range(16):
                r, g, b, w = self.np.get_pixel_color(idx)
                self.np.set_pixel_color(idx, r, green, b, w)
                green -= 16
                idx = dec_pix(idx)
        
        if (self.time_now.hour != self.time_then.hour):
            idx = hour_pixel(self.time_now.minute)
            red = 240
            for x in range(16):
                r, g, b, w = self.np.get_pixel_color(idx)
                self.np.set_pixel_color(idx, red, g, b, w)
                red -= 16
                idx = dec_pix(idx)

        self.time_then = self.time_now
        self.parent.after(200, self.update)

if __name__ == "__main__":
    ROOT = Tk()
    ROOT.title("Comet Clock")
    clock = Comet(ROOT)
    ROOT.mainloop()
