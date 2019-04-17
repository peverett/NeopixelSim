#!\usr\bin\python
"""
Transition from one LED to the Other by dmming the from LED and lighting up the Tto LED until the to LED is fully lit as the minute changes.

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

class Fade(object):

    def __init__(self, parent):

        self.np = NeopixelRing(parent, 200)
        self.time_now = datetime.now()
        self.time_then = self.time_now
        self.parent = parent

        self.__reset_second_fade()
        self.__reset_minute_fade()
        self.__reset_hour_fade()

        self.display()
        self.update()

    def __reset_second_fade(self):
        self.nsc = 0
        self.tsc = 250
        self.ns = (self.time_now.second + 1) % 60
        
    def __reset_minute_fade(self):
        self.nhc = 0
        self.thc = 240
        self.nh = (self.time_now.hour + 1) % 12


    def display(self):
        "Initially, only display Minute of hour at full brightness."
        for pixel in range(len(self.np.pixels)):
            if (pixel%5) == 0:
                self.np.set_pixel_color(pixel, 0, 0, 0, 100)

        white = lambda x: 100 if (x%5)==0 else 0

        self.np.set_pixel_color(
                self.time_now.second,
                0, 0, self.tsc, 
                white(self.time_now.second)
                )
        self.np.set_pixel_color(
                self.time_now.minute, 
                0, self.tmc, 0, 
                white(self.time_now.minute)
                )

        self.time_then = self.time_now

    def update(self):
        self.time_now = datetime.now()

        if self.time_now.second != self.time_then.second:
            self.__reset_second_fade()
        
            r, g, b, w = self.np.get_pixel_color(self.time_now.second)
            self.np.set_pixel_color(
                    self.time_now.second, r, g, self.tsc, w
                    )
            r, g, b, w = self.np.get_pixel_color(self.time_then.second)
            self.np.set_pixel_color(
                    self.time_then.second, r, g, 0, w
                    )

            if self.time_now.minute != self.time_then.minute:
                self.__reset_minute_fade()

                r, g, b, w = self.np.get_pixel_color(self.time_now.minute)
                self.np.set_pixel_color(
                        self.time_now.minute, r, self.tmc, b, w
                        )
                r, g, b, w = self.np.get_pixel_color(self.time_then.minute)
                self.np.set_pixel_color(
                        self.time_then.minute, r, 0, b, w
                        )
            else:
                r, g, b, w = self.np.get_pixel_color(self.time_now.minute)
                self.np.set_pixel_color(
                        self.time_now.minute, r, self.tmc, b, w
                        )

                r, g, b, w = self.np.get_pixel_color(self.nm)
                self.np.set_pixel_color(
                        self.nm, r, self.nmc, b, w
                        )
                self.nmc = self.nmc + 4 if self.nmc < 240 else 240
                self.tmc = self.tmc - 4 if self.tmc > 0 else 0

        else:
            r, g, b, w = self.np.get_pixel_color(self.time_now.second)
            self.np.set_pixel_color(
                    self.time_now.second, r, g, self.tsc, w
                    )

            r, g, b, w = self.np.get_pixel_color(self.ns)
            self.np.set_pixel_color(
                    self.ns, r, g, self.nsc, w
                    )
            self.nsc = self.nsc + 10 if self.nsc < 250 else 250
            self.tsc = self.tsc - 10 if self.tsc > 0 else 0


        self.time_then = self.time_now
        self.parent.after(40, self.update)
  
if __name__ == "__main__":
    ROOT = Tk()
    ROOT.title("Fade Clock")
    clock = Fade(ROOT)
    ROOT.mainloop()
