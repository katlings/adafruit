# Gemma IO demo
# Welcome to CircuitPython 2.2.4 :)

from touchio import TouchIn
import microcontroller
import neopixel
import board
import time

num_pixels = 16
pixels = neopixel.NeoPixel(board.A1, num_pixels, brightness=0.02, auto_write=False)

touch2 = TouchIn(board.A2)
touch0 = TouchIn(board.A0)

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
 
 
def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)
 
 
def rainbow_cycle(wait):
    for j in range(255):
        rainbow_step(j, wait)


def rainbow_step(j, wait):
    for i in range(num_pixels):
        print(i,j)
        rc_index = (i * 256 // num_pixels) + j
        pixels[i] = wheel(rc_index & 255)
    pixels.show()
    time.sleep(wait)


######################### MAIN LOOP ##############################

for i in range(num_pixels):
    pixels[i] = (255, 255, 255)

brightness = 0.0

while True:
    if pixels.brightness != brightness:
        pixels.brightness = brightness
        pixels.show()
        
    if touch2.value and brightness <= 1:
        brightness += 0.01
        print(brightness)

    if touch0.value:
        brightness = 0
