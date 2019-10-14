###### CODE FOR THE NEO PIXELS AND THE LEDS ######

#import packages
from __future__ import division

import re
import sys
import os
import numpy as np

########### don't need these packages ###########
# from google.cloud import speech
# from google.cloud.speech import enums
# from google.cloud.speech import types
# import pyaudio #for recording audio!
# import pygame  #for playing audio
# from six.moves import queue
# from gtts import gTTS

import time
from adafruit_crickit import crickit
from adafruit_seesaw.neopixel import NeoPixel

num_pixels = 9  # we're only using one neopixel for the gemstone

# The following line sets up a NeoPixel strip on Seesaw pin 20 for Feather
pixels = NeoPixel(crickit.seesaw, 20, num_pixels)

# the cover neo pixel is pixels[8]
#the inner pixsels are pixels[0:8]

ss = crickit.seesaw

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PALEBLUE = (70, 100, 100)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF_WHITE = (50, 50, 50)
OFF = (0,0,0)
    
def SagaReady():
    
    print ("Play lgihts?")
    duration = 10
    perc = duration / 100

    for i in range(11):
        pixels[8] = fade(OFF, OFF_WHITE, i * perc)
        time.sleep(0.1)
    for i in range(11):
        pixels[8] = fade(OFF_WHITE, WHITE, i * perc)
        time.sleep(0.1)
    for i in range(11):
        pixels[8] = fade(WHITE, OFF_WHITE, i * perc)
        time.sleep(0.1)
    for i in range(11):
        pixels[8] = fade(OFF_WHITE, WHITE, i * perc)
        time.sleep(0.1)
    for i in range(11):
        pixels[8] = fade(WHITE, OFF_WHITE, i * perc)
        time.sleep(0.1)
    for i in range(11):
        pixels[8] = fade(OFF_WHITE, OFF, i * perc)
        time.sleep(0.1)

def Warrior():
    pixels.fill(GREEN)
    time.sleep(0.3)
    pixels.fill(CYAN)
    time.sleep(0.3)
    pixels.fill(GREEN)
    
def Magician():
    pixels.fill(BLUE)
    time.sleep(0.3)
    pixels.fill(PURPLE)
    time.sleep(0.3)
    pixels.fill(BLUE)
    
def SagaOff():
    pixels.fill(OFF)

# at end of audio file
def WaitingForReply():

    pass

# received voice audio that links to some fork
def AcceptedReply():
    pass


def fade(colour1, colour2, percent):
    colour1 = np.array(colour1)
    colour2 = np.array(colour2)
    vector = colour2-colour1
    newcolour = (int((colour1 + vector * percent)[0]), int((colour1 + vector * percent)[1]), int((colour1 + vector * percent)[2]))
    return newcolour

    
# TODO add the other stories' colours and the LED code for the pages 