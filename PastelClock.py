#!\usr\bin\python
"""
Pastel clock - pretty colours.

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

class Pastel(object):

    def __init__(self, parent):

        self.np = NeopixelRing(parent, 200)
        self.time_now = datetime.now()
        self.time_then = self.time_now
        self.parent = parent
        
        self.display()
        self.parent.after(200, self.update)

    def wheel(self, pixel, cidx):
        rgbw = list(self.np.get_pixel_color(pixel))
        rgbw[cidx] = 250
        
        self.np.set_pixel_color(pixel, rgbw[0], rgbw[1], rgbw[2], 0)

        brg = 145
        stp = -5
        for x in range(1, 60):
            idx = (pixel+x) % 60
            rgbw = list(self.np.get_pixel_color(idx))
            rgbw[cidx] = brg
            self.np.set_pixel_color(idx, rgbw[0], rgbw[1], rgbw[2], 0)
            if brg == 0:
                stp = 5
            brg = brg + stp


    def display(self):
        self.update()

    def update(self):
        self.time_now = datetime.now()
        if self.time_now.second != self.time_then.second:
            self.wheel(self.time_now.second, 2)
            self.wheel(self.time_now.minute, 1)
            self.wheel(hour_pixel(self.time_now.hour), 0)

            self.time_then = self.time_now
        self.parent.after(200, self.update)
  
if __name__ == "__main__":
    ROOT = Tk()
    ROOT.title("Pastel Clock")
    clock = Pastel(ROOT)
    ROOT.mainloop()
