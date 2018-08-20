# Gemma IO demo
# Welcome to CircuitPython 2.2.4 :)

from adafruit_hid.mouse import Mouse
from touchio import TouchIn
import adafruit_dotstar as dotstar
import board
import time

dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dot.brightness = 0
dot.show()

mouse = Mouse()

touch0 = TouchIn(board.A0)
touch1 = TouchIn(board.A1)
touch2 = TouchIn(board.A2)

######################### HELPERS ##############################


######################### MAIN LOOP ##############################

clicking = False

while True:
    if not clicking and touch0.value:
        mouse.press(Mouse.RIGHT_BUTTON)
        clicking = True
    if clicking and not touch0.value:
        mouse.release_all()
        clicking = False

    if touch2.value:
        if touch1.value:
            # move up
            mouse.move(y=3)
        else:
            # move down
            mouse.move(y=-3)
