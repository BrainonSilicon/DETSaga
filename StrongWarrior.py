from utilsgit import playAudio
#some of these imports my be un-needed
#from __future__ import division

import re
import sys
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio # for recording audio!
import pygame  #for playing audio
from six.moves import queue

from gtts import gTTS
import os
import time
from adafruit_crickit import crickit


STORY_VARIABLES = {}

def PlayCurrentFork(currForkKey, variables={}):
    global STORY_VARIABLES
    print("Playing current fork {}".format("currForkKey"))

    STORY_VARIABLES = variables
    curr_fork = STORY_FORKS[currForkKey]
    currFork()

###### TODO change these to the recorded story audio files 
def Intro():
    playAudio("SWTestIntro.mp3")

def Stone():
    playAudio("SWTestForkA.mp3")

def Clay():
    playAudio("SWTestForkB.mp3")
    
def Friend(): 
    playAudio("SWTestForkAa.mp3")
    
def StayInside(): 
    playAudio("SWTestForkAb.mp3")

 
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