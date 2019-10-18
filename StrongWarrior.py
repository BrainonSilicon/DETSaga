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


STORY_VARIABLES = {}

def PlayCurrentFork(CurrFork, variables={}):
    print("Playing current fork")
    STORY_VARIABLES = variables
    currFork()

###### TODO change these to the recorded story audio files 
def Intro():
    pygame.mixer.init()
    pygame.mixer.music.load("SWTestIntro.mp3")
    pygame.mixer.music.play()

def Stone():
    pygame.mixer.init()
    pygame.mixer.music.load("SWTestForkA.mp3")
    pygame.mixer.music.play()

def Clay():
    pygame.mixer.init()
    pygame.mixer.music.load("SWTestForkB.mp3")
    pygame.mixer.music.play()
    
def Friend(): 
    pygame.mixer.init()
    pygame.mixer.music.load("SWTestForkAa.mp3")
    pygame.mixer.music.play()
    
def StayInside(): 
    pygame.mixer.init()
    pygame.mixer.music.load("SWTestForkAb.mp3")
    pygame.mixer.music.play()
 
 
##### THESE ARE THE PROMPTS #####   
# def ForkAPrompt(): 
#     pygame.mixer.init()
#     pygame.mixer.music.load("ForkAPrompt.mp3")
#     pygame.mixer.music.play()

# def ForkAaPrompt(): 
#     pygame.mixer.init()
#     pygame.mixer.music.load("ForkAaPrompt.mp3")
#     pygame.mixer.music.play()  

    

#### TODO update the dictionary with the options 
    
#this is the dictionary 
STORY_FORKS = {
    'Intro' : Intro,
    #these words will be what trigger the next piece of the story 
    'Stone': Stone, 
    'Clay': Clay,
    'Friend': Friend,
    'Home': StayInside,
    
}