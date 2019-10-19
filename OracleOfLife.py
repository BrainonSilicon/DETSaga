from Saga_Main import playAudio
#some of these imports my be un-needed
#from __future__ import division

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

def PlayCurrentFork(CurrFork, variables={}):
    print("Playing current fork")
    STORY_VARIABLES = variables
    currFork()
    
def Intro():
    pygame.mixer.init()
    pygame.mixer.music.load("OracleOfLife.mp3")
    pygame.mixer.music.play()
    
STORY_VARIABLES = {'Intro' : Intro}