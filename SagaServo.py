#THIS WILL BE SAGA'S MOTOR FUNCTIONS

#import packages 
import time
from adafruit_crickit import adafruit_crickit

def SagaClosed():
    print("Saga is closed")
    crickit.servo_1.angle = 0

def SagaOpens():
    print ("Saga opens")
    crickit.servo_1.angle = 160 #Saga can open to 165
