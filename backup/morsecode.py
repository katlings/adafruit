# Send morse code over serial

from digitalio import DigitalInOut, Direction
from touchio import TouchIn
import adafruit_dotstar as dotstar
import board
import time

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dot.brightness = 0

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Capacitive touch
touch0 = TouchIn(board.A0)
touch1 = TouchIn(board.A1)
touch2 = TouchIn(board.A2)

# based on experimentation. anything less than 500 loops is a 'dit', anything more is a 'dah'
dash_length = 500

morse_code_dict = {
    '.-': 'a',
    '-...': 'b',
    '-.-.': 'c',
    '-..': 'd',
    '.': 'e',
    '..-.': 'f',
    '--.': 'g',
    '....': 'h',
    '..': 'i',
    '.---': 'j',
    '-.-': 'k',
    '.-..': 'l',
    '--': 'm',
    '-.': 'n',
    '---': 'o',
    '.--.': 'p',
    '--.-': 'q',
    '.-.': 'r',
    '...': 's',
    '-': 't',
    '..-': 'u',
    '...-': 'v',
    '.--': 'w',
    '-..-': 'x',
    '-.--': 'y',
    '--..': 'z',
    '.----': '1',
    '..---': '2',
    '...--': '3',
    '....-': '4',
    '.....': '5',
    '-....': '6',
    '--...': '7',
    '---..': '8',
    '----.': '9',
    '-----': '0',
}

i = 0
touching = False
letter_buffer = []
output = False

while True:
    led.value = touch2.value
    i += 1

    # send tweet
    if touching and touch2.value:
        if i > dash_length * 10:
            print('EOF')
            touching = False
            output = False
            i = 0
            time.sleep(1)

    # has the state changed?
    if touching and not touch2.value:
        # we just stopped touching it
        # read how long it was touched 
        if i < dash_length:
            letter_buffer.append('.')
        else:
            letter_buffer.append('-')
        touching = False
        i = 0

    if not touching and touch2.value:
        # we just started touching it
        touching = True
        i = 0

    if not touching and not touch2.value:
        if touch0.value:
            print('BACK')
            time.sleep(0.5)
        elif touch1.value:
            print('SPACE')
            time.sleep(0.5)
        elif i > dash_length and letter_buffer:
            letter = ''.join(letter_buffer)
            letter_buffer = []
            l = morse_code_dict.get(letter)
            if l:
                print(l)
                output = True
