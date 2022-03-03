# https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
# https://lastminuteengineers.com/arduino-sr04-ultrasonic-sensor-tutorial/ 
# https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
# https://stackoverflow.com/questions/13293269/how-would-i-stop-a-while-loop-after-n-amount-of-time
# https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/5
# https://github.com/waveform80/picamera/issues/488
# https://www.codingem.com/try-catch-in-python/
# https://www.geeksforgeeks.org/errors-and-exceptions-in-python/
# https://www.w3schools.com/python/python_try_except.asp

#Libraries
from picamera import PiCamera
from plateReader import readPlate
from parkIn import park_car
import RPi.GPIO as GPIO
import time

try: 
    #Cam settings
    camera = PiCamera()
    camera.resolution = (2592, 1944)
except:
    print("camera down")
else:
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
     
    #set GPIO Pins
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24
     
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    timeout = 5
# if timeout, return -1000
def distance():
    ts = time.time()
    #print("before sending pulse")
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    #print("trigger is high")
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    #print("done sending pulse")
    
    StartTime = time.time()
    StopTime = time.time()
     
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        if StartTime > ts + timeout:
            return -1000
 
    # print("signal sent, ECHO is high")
    # save time of arrival
    # time.sleep(10)
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        if StopTime > ts + timeout:
            return -1000
    # print("signal received, ECHO is low")
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    #print(f"time elapsed: {TimeElapsed}")
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        prevDist = 1200
        while True:
            dist = distance()
            print(f"distance is: {dist}")
            if dist < 0:
                print("Motion sensor broken")
            elif dist > 1200:
                print("Nothing within range")
            else:
                if prevDist > dist + 10:
                    if prevDist >= 1200:
                        print("Something showed up")
                    else:
                        print(f"Something is approaching from {prevDist} cm to {dist} cm")
                elif abs(prevDist - dist) <= 5 and dist < 100:
                    print(f"Obj stopped at a close range")
                    try:
                        camera.capture(f"/home/pi/Desktop/obj.jpg")
                        plateNum = readPlate("/home/pi/Desktop/obj.jpg")
                        #print("cv finished")
                        if len(plateNum) != 0:
                            rows_affected = park_car(plateNum)
                            print(f"{rows_affected} rows changed")
                    except:
                        print("camera down")
                    else:
                        print("Success")
            prevDist = dist
            time.sleep(5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()