#!\usr\bin\python
"""
Simulate, very approximately, a neopixel ring of 60 neopixels using python and
Tkinter.

Using this approimate neopixel simulation, I can try out various clock display
designs before implementing them using an Ardiuno and real Neopixel hardware.

Python 2.7, 3.6 compatible.
"""
from __future__ import print_function

import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

import math
from datetime import datetime

def hour_pixel(hour):
    """Translate the current hour (0..23) into its pixel offset (0..59)"""
    val = hour if hour<12 else hour -12
    return val * 5

class NeopixelRing(object):
    "Simulates a 60 LED Neopixel ring or string"

    def __init__(self, parent, radius):
        self.parent = parent
        self.radius = radius
        self.centre = radius + 20
        self.size = self.centre * 2

        self.canvas = Canvas(parent, height=self.size, width=self.size)
        self.canvas.config(bg='black')
        self.canvas.pack()
        self.pixels = []

        self.draw_neopixels()

    def draw_neopixels(self):
        "Draw the neopixels as circles"

        # To draw the ring from the top, start at 270 degrees round to 0,
        # then add degrees from 0 to 270.
        angles = [x for x in range(270, 360, 6)]
        angles.extend([x for x in range(0, 270, 6)])

        # For each neopixel store the Tkinter object ID and the Red, Green,
        # Blue and White values (should be in range 0..255).
        pixel  = {"id": 0, "r": 0, "g": 0, "b": 0, "w": 0}
        for angle in angles:
            x = self.radius * math.cos(math.radians(angle))
            y = self.radius * math.sin(math.radians(angle))

            pixel["id"] = self.canvas.create_oval(
                        round(x + self.centre - 10), 
                        round(y + self.centre - 10),
                        round(x + self.centre + 10),
                        round(y + self.centre + 10),
                        fill='black'
                        )
            self.pixels.append(pixel.copy())

    def set_pixel_color(self, idx, red, green, blue, white):
        "Set the individual neopixel's colour (simulated)."
        if idx < len(self.pixels):

            # Store the pixel color
            pixel = self.pixels[idx]
            pixel["r"] = red
            pixel["g"] = green
            pixel["b"] = blue
            pixel["w"] = white

            # Neopixel colours are 8-bit but in tkinter they are 12-bit so
            # Multiply by 12 to get approximate range.
            s_red = (red+white)*16
            s_green = (green+white)*16
            s_blue = (blue+white)*16

            s_red = s_red if s_red <= 0xFFF else 0xFFF
            s_green = s_green if s_green <= 0xFFF else 0xFFF
            s_blue = s_blue if s_blue <= 0xFFF else 0xFFF

            colour = (s_red << 24) | (s_green) << 12 | (s_blue)

            self.canvas.itemconfig(pixel["id"], fill='#{:09x}'.format(colour))

    def get_pixel_color(self, idx):
        "Get the pixel colour, as previously stored when set."
        if idx < len(self.pixels):
            pixel = self.pixels[idx]

            return (pixel["r"], pixel["g"], pixel["b"], pixel["w"])
        else:
            return (0, 0, 0, 0)

if __name__ == "__main__":
    
    class Test(object):
        """Simplest test class - display colours around the ring...
                white at 12 o'clock
                red at 3 o'clock
                green at 6 o'clock
                blue at 9 o'clock"""
        
        def __init__(self, parent):
            self.parent = parent
            self.np = NeopixelRing(parent, 200)

            self.np.set_pixel_color(0, 0, 0, 0, 255)
            self.np.set_pixel_color(15, 255, 0, 0, 0)
            self.np.set_pixel_color(30, 0, 225, 0, 0)
            self.np.set_pixel_color(45, 0, 0, 255, 0)
    

    ROOT = Tk()
    ROOT.title("NeopixelSim")
    clock = Test(ROOT)
    ROOT.mainloop()

