##SET UP!! 

#IMPORT PACKAGES 
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
import time
from adafruit_crickit import crickit
from adafruit_seesaw.neopixel import NeoPixel

#IMPORT SAGA'S FILES
import saga_lights
import saga_servo
#TODO import the story files
import StrongWarrior

# Audio recording parameters, set for our USB mic.
RATE = 44100 #if you change mics - be sure to change this :)
CHUNK = int(RATE / 10)  # 100ms

#import credentials 
credential_path = "/home/pi/DET190-JSON/DETcredential.json" #TODO change this to who'sever pi we're using
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credential_path

#THIS IS VERY IMPORTANT AS THE API LOOKS FOR IT 
client = speech.SpeechClient()

#initialize pygame so that I can run audio 
pygame.init()
pygame.mixer.init()


#### STORY  GLOBAL VARIABLES ################################
#############################################################
CURR_STORY = None
STORY_VARIABLES = {}
#isListening = False # TODO this might need to be taken out

#MicrophoneStream() is brought in from Google Cloud Platform
class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self
    
    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()    
   
   #the buffer is an array that holds the audio data (ie. from the stream)
    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer.""" #TODO THIS SHIT NEEDS TO BE CHANGED
        self._buff.put(in_data)
        return None, pyaudio.paContinue
    
    def generator(self):
            while not self.closed:
                # Use a blocking get() to ensure there's at least one chunk of
                # data, and stop iteration if the chunk is None, indicating the
                # end of the audio stream.
                chunk = self._buff.get()
                if chunk is None:
                    return
                data = [chunk]

                # Now consume whatever other data's still buffered.
                while True:
                    try:
                        chunk = self._buff.get(block=False)
                        if chunk is None:
                            return
                        data.append(chunk)
                    except queue.Empty:
                        break

                yield b''.join(data)


#this loop is where the microphone stream gets sent
# TODO look at with Varda so that it's only called when an audio file is not playing 
def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
#            sys.stdout.write(transcript + overwrite_chars + '\r')
#            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            #if there's a voice activitated quit - quit!
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break
            else:
                story_decision(transcript)
#            print(transcript)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            num_chars_printed = 0

            
def story_decision(transcript):
    global CURR_STORY
    print("is audio playing? : {}".format(pygame.mixer.music.get_busy()))
    
    if pygame.mixer.music.get_busy():
        return
    
    print("Current Story : {}".format(CURR_STORY))
    if CURR_STORY:
        forks = CURR_STORY.STORY_FORKS.keys()
        for fork in forks:
            if re.search(fork, transcript, re.I):
                print("the fork selected is: {}",format(fork))
                curr_fork = CURR_STORY.STORY_FORKS[fork]   
                CURR_STORY.PlayCurrentFork(curr_fork) 

  #IF THE KID RESPONDS "strong warrior", gTTs matches, and the StrongWarrior file plays
    elif re.search("strong", transcript, re.I):
        CURR_STORY = StrongWarrior
        curr_fork = CURR_STORY.STORY_FORKS['intro'] #this might need to change to be changing based on where it is (eg. i) 
        CURR_STORY.PlayCurrentFork(curr_fork)

    #TODO elif statements for the other story options 


def playAudio(text):
    text2Speech = gTTS(text, lang ='en')
    text2Speech.save('audioFile.mp3')
    
    pygame.mixer.init()
    pygame.mixer.music.load('audioFile.mp3')
    pygame.mixer.music.play()


def playTextToAudio(text):
    #TODO: read in the text and play it as an audio file
    #google text to speech: check viviks example
    # pass
    t2s = gTTS(text, lang ='en')
    t2s.save('Start.mp3')


def Main():
    #initialize things 
    language_code = 'en-US'  # a BCP-47 language tag
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)
    
    #this section is where the action for the gTTs happens:
    #give the intro 
    playAudio('What kind of story do you want to hear tonight?')
    
    #mic set up to look for input and the info is sent to google for analysis 
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)
        listen_print_loop(responses)


    #give the intro 
    # SagaIntro()
    #wait for the user's input 
    # story_decision()
    
    
    
    
    if __name__ == '__main__':
        Main()
    
    
    
    
    
