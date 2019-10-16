from Saga_Main import PlayAudio
#some of these imports my be un-needed
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


STORY_VARIABLES = {}
#this is the dictionary 
STORY_FORKS = {
    'intro' : Intro,
    #these words will be what trigger the next piece of the story 
    'story': A, 
    #'word_aa': AA,
    #'word_ab': AB
}

def PlayCurrentFork(currFork, variables={}):
    STORY_VARIABLES = variables
    STORY_FORKS[currFork]()

    
def Option1:
    # this is not the actual code playTextToAudio("Do you want a clay house or a stone house?")
    
        
def main():
    
    #setting up the GTTS responses as .mp3 files!
    t2s = gTTS("Hello brave warrior, let's go on an adventure.", lang ='en')
    t2s.save('helloWarrior.mp3')
    #t2s = gTTS('You didnt tell me what to do with that.', lang='en')
    #t2s.save('idontknow.mp3')
    
    language_code = 'en-US'  # a BCP-47 language tag

    #set up a client
    #make sure GCP is aware of the encoding, rate 
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    #our example uses streamingrecognition - most likely what you will want to use.
    #check out the simpler cases of asychronous recognition too!
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)
    