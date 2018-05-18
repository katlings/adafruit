# Just matches capacitive touch inputs to Overwatch hotkeys: Shift, E, Q
# Wire up some custom touchpads (bananas, anyone?) and it could be fun :)

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from touchio import TouchIn
import adafruit_dotstar as dotstar
import board
import time

# Turn the bright light off
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dot.brightness = 0
dot.show()

# Capacitive touch
touch0 = TouchIn(board.A0)
touch1 = TouchIn(board.A1)
touch2 = TouchIn(board.A2)

kbd = Keyboard()

######################### MAIN LOOP ##############################

# TODO: hold down button as long as the pad is touched
# TODO: Use a Circuit Playground for more fun tools like more inputs and an accelerometer

while True:
  if touch0.value:
        kbd.press(Keycode.Q)
        kbd.release_all()
        time.sleep(1)
  elif touch1.value:
        kbd.press(Keycode.SHIFT)
        kbd.release_all()
        time.sleep(1)
  elif touch2.value:
        kbd.press(Keycode.E)
        kbd.release_all()
        time.sleep(1)
