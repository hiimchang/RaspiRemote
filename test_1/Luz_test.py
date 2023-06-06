# import os
# from gpiozero import LED, Button
# from signal import pause
#
# print(os.path.abspath(__file__))
#
#
# def say_hello():
#     print("Hello")
#
#
# led = LED(18)
# button = Button(2)
# print("Press button")
# button.when_pressed = say_hello
# button.when_pressed = led.on()
# button.when_released = led.off()
# pause()


from gpiozero import Button

from signal import pause

import board

import neopixel

import time


def lights():
    print("Button pressed")

    # red

    pixels[0] = (255, 0, 0)

    time.sleep(2)

    pixels[0] = (0, 0, 0)

    # green

    pixels[1] = (0, 255, 0)

    time.sleep(2)

    pixels[1] = (0, 0, 0)

    # blue

    pixels[2] = (0, 0, 255)

    time.sleep(2)

    pixels[2] = (0, 0, 0)


pixels = neopixel.NeoPixel(board.D18, 5)

button = Button(2)

print("Press button")

button.when_pressed = lights

pause()
