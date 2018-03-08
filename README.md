# NeopixelSim

Simulates, very approximately, an Adafruit RGBW Neopixel Ring (or Strip) 
with 60 Neopixels using the Python Tkinter library.

What you get is a simple graphic display simulation of the Neopixel ring.

The NeopixelRing class has a very basic API similar to the [Adafruit 
C++ Library for Neopixels](https://github.com/adafruit/Adafruit_NeoPixel). 

All you get is...
* set_pixel_color(index, Red, Green, Blue, White): Returns None
* get_pixel_color(index): Returns tuple Red, Green, Blue, White

In the real Adafruit C++ lib, the colour is returned as 32-bit integer that you
must mask and shift to get the individual colour values.

The colours (Red, Green, Blue, White) are in the range 0 to 255 (as it is for 
real neopixels). 

I wrote this to try out different ways of displaying the time, for making a
neopixel clock, and for that, this is surprisingly effective. 

Several clock display examples are included.
