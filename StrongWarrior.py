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

<<<<<<< HEAD
def PlayCurrentFork(CurrFork, variables={}):
=======
def PlayCurrentFork(currFork, variables={}):
    global STORY_VARIABLES
>>>>>>> 7b63f50516b5446ad63994510c22fabb06ee09bb
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

    

<<<<<<< HEAD
#### TODO update the dictionary with the options 
    
#this is the dictionary 
STORY_FORKS = {
    'Intro' : Intro,
    #these words will be what trigger the next piece of the story 
    'Stone': Stone, 
    'Clay': Clay,
    'Friend': Friend,
    'Home': StayInside,
    
=======
#this is the dictionary
STORY_FORKS = {
    'intro' : intro,
    #these words will be what trigger the next piece of the story
    'stone': stone,
    #'word_aa': AA,
    #'word_ab': AB
>>>>>>> 7b63f50516b5446ad63994510c22fabb06ee09bb
}