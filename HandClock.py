#!\usr\bin\python
"""
Simulate the hands of a clock - Size matters
- Hours is 5 pixels, brightest in the middle pixel.
- Minutes is 3 pixels.
- Seconds is 1-pixe.
The hands occlude each other e.g. minutes on top of hours and seconds on top of
minutes.
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

class Hands(object):

    def __init__(self, parent):

        self.np = NeopixelRing(parent, 200)
        self.time_now = datetime.now()
        self.time_then = self.time_now
        self.parent = parent
        
        self.display()
        self.parent.after(200, self.update)

    def hour_hand(self, hour):
        for x in range(-2,3,1):
            idx = (hour_pixel(hour)+x) % 60

            intensity = 250 - (abs(x) * 50)
            self.np.set_pixel_color(idx, intensity, 0, 0, 0)

    def minute_hand(self, minute):
        for x in range(-1,2,1):
            idx = (minute+x) % 60

            intensity = 250 - (abs(x) * 50)
            self.np.set_pixel_color(idx, 0, intensity, 0, 0)

    def second_hand(self, second):
        self.np.set_pixel_color(second, 0, 0, 250, 0)

    def display(self):
        self.hour_hand(self.time_now.hour)
        self.minute_hand(self.time_now.minute)
        self.second_hand(self.time_now.second)
        self.time_then = self.time_now

    def update(self):
        self.time_now = datetime.now()
        if self.time_now.second != self.time_then.second:

            for pixel in range(len(self.np.pixels)):
                self.np.set_pixel_color(pixel, 0, 0, 0, 0)

            self.hour_hand(self.time_now.hour)
            self.minute_hand(self.time_now.minute)
            self.second_hand(self.time_now.second)

            self.time_then = self.time_now
        self.parent.after(200, self.update)
  
if __name__ == "__main__":
    ROOT = Tk()
    ROOT.title("Hands Clock")
    clock = Hands(ROOT)
    ROOT.mainloop()
