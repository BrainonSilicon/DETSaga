from utils import playAudio
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


def PlayCurrentFork(currForkKey, variables={}):
    print("Playing current fork {}".format("currForkKey"))
    curr_fork = STORY_FORKS[currForkKey]
    curr_fork()
    
def Intro():
    playAudio("Saga_Audio_Files/NewCleverMagicianIntro.mp3")
    
def River():
    playAudio("Saga_Audio_Files/CleverMagicianForkA.mp3")
    
def Valley():
    playAudio("Saga_Audio_Files/Norm_NewValley.mp3")
    
def NoFork():
    playAudio("Saga_Audio_Files/TestNoForkWritten.mp3")
    
def Mirror():
    playAudio("Saga_Audio_Files/NewMagicianAfterMirror.mp3")
    
STORY_FORKS = {
    'Intro' : Intro,
    'Right': River,
    'River': River,
    'Figure': NoFrok,
    'Ghost': NoFork,
    'Left': Valley,
    'Valley': Valley,
    'Yes': Mirror,
    'No': Mirror,
    'Arch': NoFork,
    'Sand': NoFork
}


