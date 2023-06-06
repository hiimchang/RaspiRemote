from gpiozero import Button
from signal import pause
import cv2

cap = cv2.VideoCapture(0)
i = 0


def held():
    global i
    print("Button pressed")
    ret, frame = cap.read()
    if ret:
        outfile = '/home/ubuntu/RaspiRemote/images/image_' + str(i) + '.jpg'
        cv2.imwrite(outfile, frame)
        i += 1


button = Button(2)
print("Press the button 2 seconds")
button.when_held = held
pause()
