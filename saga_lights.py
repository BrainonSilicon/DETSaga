###### CODE FOR THE NEO PIXELS AND THE LEDS ######

#import packages
from __future__ import division

import re
import sys
import os

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

# TODO : import the LED packages and set up the LEDS 
 
num_pixels = 1  # we're only using one neopixel for the gemstone
 
# The following line sets up a NeoPixel strip on Seesaw pin 20 for Feather
pixels = NeoPixel(crickit.seesaw, 20, num_pixels)

ss = crickit.seesaw

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0,0,0)

def Saga_ready():
    pixels.fill(WHITE)

def Warrior():
    pixels.fill(GREEN)
    
# TODO add the other stories' colours and the LED code for the pages 