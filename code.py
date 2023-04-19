import board
import digitalio
import analogio
import usb_hid
from time import sleep

from hid_gamepad import Gamepad

gp = Gamepad(usb_hid.devices)
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

button_pins = (board.GP14, board.GP15)
gamepad_buttons = (1, 2)

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
buttons_pressed = [False for pin in button_pins]

for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

while True:
    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]
        if not button.value and buttons_pressed[i] == False:
            buttons_pressed[i] = True
            print('button pressed')
            gp.press_buttons(gamepad_button_num)
            led.value = True
        elif button.value and buttons_pressed[i] == True:
            buttons_pressed[i] = False
            print('button released')
            gp.release_buttons(gamepad_button_num)
            led.value = False
    sleep(.1)
