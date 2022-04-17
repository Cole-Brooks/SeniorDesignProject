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
from readPlate import readPlate
from parkIn import *
import RPi.GPIO as GPIO
import time
import picamera
from sendAlert import send_alert
import os

needFix = False
# initialize camera
try: 
    #Cam settings
    camera = PiCamera()
    camera.resolution = (2592, 1944)
except:
    print("camera down")
    needFix = True
else:
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
     
    #set GPIO Pins
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24
    GPIO_GATE = 25
    
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(GPIO_GATE, GPIO.OUT)
    
    timeout = 5
    
gateOpening = False
gateClosing = False
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
 
def parkingLogic(statVar, plfVar, plodVar, plAddr):
    global needFix, gateOpening, gateClosing
    while statVar == None:
        pass
    try:
        prevDist = 1200
        statVar.set(f"Status: {getStat(plAddr)}")
        while True:
            dist = distance()
            print(f"distance is: {dist}")
            plfVar.set(f"Fee per Hour: {get_fee_info(plAddr)}$")
            plodVar.set(f"Max Overdue: {get_overdue_info(plAddr)}")
            if dist < 0:
                print("Motion sensor broken")
                needFix = True
                statVar.set(f"Status: {getStat(plAddr)}")
            elif dist > 1200:
                needFix = False
                print("Nothing within range")
                statVar.set(f"Status: {getStat(plAddr)}")
            else:
                needFix = False
                if prevDist > dist + 10:
                    if prevDist >= 1200:
                        print("Something showed up")  
                    else:
                        print(f"Something is approaching from {prevDist} cm to {dist} cm")
                    statVar.set(f"Status: {getStat(plAddr)}")
                elif abs(prevDist - dist) <= 5 and dist < 100:
                    print(f"Obj stopped at a close range")
                    statVar.set("Status: Please Wait")
                    try:
                        camera.capture(f"/home/pi/Desktop/obj.jpg")
                        plateNum, confi = readPlate("/home/pi/Desktop/obj.jpg")
                        print(plateNum, confi)
                        #os.remove(f"/home/pi/Desktop/obj.jpg")
                        #print("cv finished")
                        if confi > 0.9:
                            statVar.set("Status: Parking " + plateNum)
                            res = park_car(plateNum, plAddr)
                            print(res)
                            time.sleep(1)
                            statVar.set("Status: " + res)
                            time.sleep(1)
                            if res[0] == 'S':  
                                statVar.set("Status: Drive Through")
                                GPIO.output(GPIO_GATE, 1);
                                time.sleep(1)
                                GPIO.output(GPIO_GATE, 0);
                                time.sleep(23)
                                GPIO.output(GPIO_GATE, 1);
                                time.sleep(1)
                                GPIO.output(GPIO_GATE, 0);
                            
                                #gateClosing = True
                                statVar.set("Status: Please Wait for Your Turn")
                                time.sleep(13);
                                #gateClosing = False
                                statVar.set(f"Status: {getStat(plAddr)}")
                        elif confi == -1:
                            statVar.set("Status: " + plateNum)
                        else:
                            statVar.set("Status: Wait for Rescan")
                    except picamera.PiCameraError:
                        print("Camera down")
                        needFix = True
                        statVar.set(f"Status: {getStat(plAddr)}")
                else:
                    statVar.set(f"Status: Please Come Closer")
            prevDist = dist
            time.sleep(2)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


def getStat(plAddr):
    if needFix:
        print("needFix")
        phoneNum = get_admin_contactInfo(plAddr)[2:];
        send_alert('Alert', f'Parking Lot in {plAddr} need Maintainance', phoneNum)
        return "Maintainance"
    if get_free_spots(plAddr) == 0:
        return "Full"
    return "Available"