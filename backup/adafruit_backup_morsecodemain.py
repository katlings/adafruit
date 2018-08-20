# Gemma IO demo
# Welcome to CircuitPython 2.2.4 :)

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn, AnalogOut
from touchio import TouchIn
import adafruit_dotstar as dotstar
import microcontroller
import board
import time

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dot.brightness = 0

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Analog output on A0
aout = AnalogOut(board.A0)

# Analog input on A1
analog1in = AnalogIn(board.A1)

# Capacitive touch on A2
touch2 = TouchIn(board.A2)

# Used if we do HID output, see below
kbd = Keyboard()

######################### HELPERS ##############################

# Helper to convert analog input to voltage
def getVoltage(pin):
    return (pin.value * 3.3) / 65536

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

i = 0
touching = False

# based on experimentation. anything less than 900 loops is a 'dit', anything more is a 'dah'
threshold = 900

letter_buffer = []

morse_code_dict = {
    '.-': Keycode.A,
    '-...': Keycode.B,
    '-.-.': Keycode.C,
    '-..': Keycode.D,
    '.': Keycode.E,
    '..-.': Keycode.F,
    '--.': Keycode.G,
    '....': Keycode.H,
    '..': Keycode.I,
    '.---': Keycode.J,
    '-.-': Keycode.K,
    '.-..': Keycode.L,
    '--': Keycode.M,
    '-.': Keycode.N,
    '---': Keycode.O,
    '.--.': Keycode.P,
    '--.-': Keycode.Q,
    '.-.': Keycode.R,
    '...': Keycode.S,
    '-': Keycode.T,
    '..-': Keycode.U,
    '...-': Keycode.V,
    '.--': Keycode.W,
    '-..-': Keycode.X,
    '-.--': Keycode.Y,
    '--..': Keycode.Z,
}

while True:
    i += 1

    # has the state changed?
    if touching and not touch2.value:
        # we just stopped touching it
        # read how long it was touched 
        print("touched for", i)
        if i < threshold:
            letter_buffer.append('.')
        else:
            letter_buffer.append('-')
        touching = False
        i = 0

    if not touching and touch2.value:
        # we just started touching it
        # read how long we were silent
        print("absent for", i)
        touching = True
        i = 0

    if not touching and not touch2.value:
        if i > threshold and letter_buffer:
            letter = "".join(letter_buffer)
            letter_buffer = []
            print("read", letter)
            key = morse_code_dict.get(letter)
            if key:
                kbd.press(key)
                kbd.release_all()

    led.value = touch2.value
