import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
     
#set GPIO Pins

GPIO_GATE = 25
    
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_GATE, GPIO.OUT)

GPIO.output(GPIO_GATE, 1);
time.sleep(1)
GPIO.output(GPIO_GATE, 0);
