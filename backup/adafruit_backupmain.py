# Gemma IO demo
# Welcome to CircuitPython 2.2.4 :)

import microcontroller
import neopixel
import board
import time

ps = neopixel.NeoPixel(board.A1, 16, brightness=0.2, auto_write=False)

######################### HELPERS ##############################

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    if (pos < 85):
        return [int(pos * 3), int(255 - (pos*3)), 0]
    elif (pos < 170):
        pos -= 85
        return [int(255 - pos*3), 0, int(pos*3)]
    else:
        pos -= 170
        return [0, int(pos*3), int(255 - pos*3)]

######################### MAIN LOOP ##############################

ps.fill([255, 0, 0])
ps.brightness = 0
ps.show()
