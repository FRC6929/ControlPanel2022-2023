import board
from time import sleep
from time import monotonic as time

import digitalio
import usb_hid
import analogio
import rotaryio

from hid_gamepad import Gamepad
led = digitalio.DigitalInOut(board.LED) 
led.direction = digitalio.Direction.OUTPUT

def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

gp = Gamepad(usb_hid.devices)
coup = 3


button_pins = (board.GP6, board.GP7, board.GP8, board.GP9, board.GP5, board.GP4, board.GP3, board.GP2, board.GP10, board.GP11, board.GP12, board.GP13, board.GP17)
gamepad_buttons = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
start = 0

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
button_state = [False for pin in button_pins]

reset_button = digitalio.DigitalInOut(board.GP16)
reset_button.pull = digitalio.Pull.UP
reset_but_state = False

for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP


encoder = rotaryio.IncrementalEncoder(board.GP26, board.GP27)
last_position = None
pos = 0
real_pos = 0

while True:
    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]
        state = button_state[i]
        if button.value and state == True:
            button_state[i] = False
            gp.release_buttons(gamepad_button_num)
            print(" release", gamepad_button_num, end="")
            led.value = False
        elif not button.value and state == False:
            button_state[i] = True
            gp.press_buttons(gamepad_button_num)
            print(" press", gamepad_button_num, end="")
            led.value = True

    position = encoder.position
    if position != last_position and last_position != None:
        if(position < last_position and real_pos >= -127):
            if((real_pos - coup) < -127): 
                pos -= coup
                if(real_pos >= -127): real_pos = -127
            elif(pos > 127): pos -= coup
            else: 
                pos -= coup
                if pos < -127:
                    real_pos = -127
                else: 
                    real_pos = pos
            print(real_pos, '-10')
        elif(position > last_position and real_pos <= 127): 
            if((real_pos + coup) > 127): 
                pos += coup
                if(real_pos <= 127): real_pos = 127
            elif(pos < -127): pos += coup
            else: 
                pos += coup
                if pos > 127:
                    real_pos = 127
                else: 
                    real_pos = pos
            print(real_pos, '+10')
        else: print(real_pos)
    if(reset_button.value == False and reset_but_state == False): 
        reset_but_state = True
        start = round(time() * 1000.0)
    elif(reset_button.value and reset_but_state):
        if((round(time() * 1000.0) - start) < 500):
            pos = 0
            real_pos = pos
            last_position = 0
        print('button click', round(time()*1000.0) - start)
        reset_but_state = False
    last_position = position
    gp.move_joysticks(
        x=real_pos
    )