# import required libraries
from vidgear.gears import NetGear
import cv2

# Open suitable video stream
stream = cv2.VideoCapture(0)

# define tweak flags
options = {"flag": 0, "copy": False, "track": False}

# Define Netgear server at given IP address and define parameters
server = NetGear(
    address="10.10.10.201",
    port="5454",
    protocol="tcp",
    pattern=0,
    logging=True,
    **options
)

# loop over until KeyBoard Interrupted
while True:
    try:
        # read frames from stream
        (grabbed, frame) = stream.read()

        # check for frame if not grabbed
        if not grabbed:
            break

        # send frame
        server.send(frame)
    except KeyboardInterrupt:
        break

# safely close video stream
stream.release()

# safely close server
server.close()
