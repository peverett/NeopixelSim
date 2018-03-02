#!\usr\bin\python
"""
Simulate an analog clock with Red for hours, green for minutes and blue
for seconds.

Display the clock markings with dim white (dark grey).
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

class Analog(object):

    def __init__(self, parent):

        self.np = NeopixelRing(parent, 200)
        self.time_now = datetime.now()
        self.time_then = self.time_now
        self.parent = parent
        
        self.display()
        self.parent.after(200, self.update)

    def display(self):
        for pixel in range(len(self.np.pixels)):
            if (pixel%5) == 0:
                self.np.set_pixel_color(pixel, 0, 0, 0, 100)

        white = lambda x: 100 if (x%5)==0 else 0

        self.np.set_pixel_color(
                self.time_now.second, 
                0, 0, 255, 
                white(self.time_now.second))

        self.np.set_pixel_color(
                self.time_now.minute,
                0, 255, 0,
                white(self.time_now.minute))

        self.np.set_pixel_color(
                hour_pixel(self.time_now.hour),
                255, 0, 0,
                white(hour_pixel(self.time_now.hour)))

        self.time_then = self.time_now

    def update(self):
        self.time_now = datetime.now()
        if self.time_now.second != self.time_then.second:

            r, g, b, w = self.np.get_pixel_color(self.time_then.second)
            self.np.set_pixel_color(self.time_then.second, r, g, 0, w)

            r, g, b, w = self.np.get_pixel_color(self.time_now.second)
            self.np.set_pixel_color(self.time_now.second, r, g, 255, w)

            if self.time_now.minute != self.time_then.minute:
                r, g, b, w = self.np.get_pixel_color(self.time_then.minute)
                self.np.set_pixel_color(self.time_then.minute, r, 0, b, w)

                r, g, b, w = self.np.get_pixel_color(self.time_now.minute)
                self.np.set_pixel_color(self.time_now.minute, r, 255, b, w)

            if self.time_now.hour != self.time_then.hour:
                r, g, b, w = self.np.get_pixel_color(self.time_then.hour)
                self.np.set_pixel_color(
                        hour_pixel(self.time_then.hour), 0, g, b, w
                        )

                r, g, b, w = self.np.get_pixel_color(self.time_now.hour)
                self.np.set_pixel_color(
                        hour_pixel(self.time_now.hour), 255, g, b, w
                        )

            self.time_then = self.time_now
        self.parent.after(200, self.update)
  
if __name__ == "__main__":
    ROOT = Tk()
    ROOT.title("Analog Clock")
    clock = Analog(ROOT)
    ROOT.mainloop()
