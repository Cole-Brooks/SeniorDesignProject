# https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/5
# https://www.codingem.com/try-catch-in-python/
# https://www.geeksforgeeks.org/errors-and-exceptions-in-python/
# https://www.w3schools.com/python/python_try_except.asp

from picamera import PiCamera
from time import sleep

try:
    camera = PiCamera()
    camera.resolution = (2592, 1944)
    camera.start_preview()
    sleep(5)
    #camera.capture('/home/pi/Desktop/firstPICam.jpg')
    camera.stop_preview()
except:
    print("camera not available")
finally:
    print("testing")