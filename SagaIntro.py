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

client = speech.SpeechClient()

pygame.init()
pygame.mixer.init()


def Start():
    pygame.mixer.init()
    pygame.mixer.music.load("Saga_Audio_Files/IntroWakeUp.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): 
        pygame.time.Clock().tick(10)