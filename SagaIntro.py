#THIS IS THE FILE FOR THE START s
from __future__ import division

import re
import sys
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio #for recording audio!
import pygame  #for playing audio
from six.moves import queue

from gtts import gTTS
import os
import time
from adafruit_crickit import crickit

RATE = 44100 #TODO: change this to razer mic
CHUNK = int(RATE / 10)  # 100ms

#import credentials 
credential_path = "/home/pi/DET190-JSON/DETcredential.json" #credential file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credential_path

client = speech.SpeechClient()

pygame.init()
pygame.mixer.init()

def CreateStartAudio():
    t2s = gTTS("What kind of story do you want to hear tonight?", lang ='en')
    t2s.save('Start.mp3')

def Start():
    pygame.mixer.init()
    pygame.mixer.music.load("Start.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): 
        pygame.time.Clock().tick(10)