# Gemma IO echo server
# Tap A2 in a pattern; the board will play back the tap pattern on the red LED

from digitalio import DigitalInOut, Direction
from touchio import TouchIn
import adafruit_dotstar as dotstar
import board

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dot[0] = [0, 255, 0]

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Capacitive touch on A2
touch2 = TouchIn(board.A2)


######################### HELPERS ##############################


def playback(playback_buffer):
    i = 0
    playback_i = 0
    # It would be simpler to do this in a for loop, but it plays back too fast!
    while True:
        if playback_i >= len(playback_buffer):
            return
        i += 1
        loops, state = playback_buffer[playback_i]
        led.value = state
        if i > loops:
            playback_i += 1
            i = 0


def record():
    touching = False
    led.value = False
    i = 0
    playback_buffer = []
    THRESHOLD = 1000  # Wait this many loops before playing back

    while True:
        i += 1

        # Has the state changed?
        if touching and not touch2.value:
            # we just stopped touching it
            dot[0] = [0, 255, 0]
            dot.show()
            # read how long it was touched 
            print("touched for", i)
            playback_buffer.append((i, True))
            touching = False
            i = 0

        if not touching and touch2.value:
            # we just started touching it
            dot[0] = [0, 0, 255]
            dot.show()
            # read how long we were silent
            print("absent for", i)
            playback_buffer.append((i, False))
            touching = True
            i = 0

        # Detect pause
        if not touching and not touch2.value:
            # If we paused long enough and there's something to play back
            if i > THRESHOLD and len(playback_buffer) > 1:
                # Always start playing back with an 'on' state
                if playback_buffer[0][1] == False:
                    playback_buffer.pop(0)
                return playback_buffer


######################### MAIN LOOP ##############################


record_state = True

while True:
    if record_state:
        dot.brightness = 0.1
        dot.show()
        playback_buffer = record()
        record_state = False
    else:
        dot.brightness = 0
        dot.show()
        playback(playback_buffer)
        record_state = True
