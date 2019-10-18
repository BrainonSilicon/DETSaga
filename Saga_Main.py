######### SET UP!! ###########
##############################

#IMPORT PACKAGES 
from __future__ import division

import re
import sys
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio 
import pygame 
from six.moves import queue

from gtts import gTTS
import time
from adafruit_crickit import crickit
from adafruit_seesaw.neopixel import NeoPixel

#### IMPORT SAGA'S FILES ########
# TODO: import saga_lights
import Saga_servo

#TODO import the story files
import StrongWarrior

# Audio recording parameters, set for our USB mic.
RATE = 44100 #this works for the Razer mic but not the new DET mic
CHUNK = int(RATE / 10)  # 100ms ## TODO this also needs to be changed for the DET new mic 

#import credentials 
credential_path = "/home/pi/DET190-JSON/DETcredential.json" #TODO change this to whomever's pi we're using
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credential_path

#THIS IS VERY IMPORTANT AS THE API LOOKS FOR IT 
client = speech.SpeechClient()

#initialize pygame so that we can run audio 
pygame.init()
pygame.mixer.init()


#### STORY  GLOBAL VARIABLES #######################
####################################################
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
def ListenPrintLoop(responses):
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
            #if the kid says that they want to go to sleep - then the story stops
            if re.search(r'\b(exit|quit|sleep|tired)\b', transcript, re.I): #TODO if it breaks, check this
                print("Story is ending")
                ######### SagaNPAudio.Goodnight()
                SagaServo.SagaClosed()
                break
            #elif no reponse for 10 seconds -> prompt the question again -> if still no response then close 
            
            
            else:
                StoryDecision(transcript)
#            print(transcript)
            # Exit recognition if any of the transcribed phrases could be one of the key words so it should be fine #
            num_chars_printed = 0

###### THIS IS THE ELIF THAT MAKES THE STORIES!! #########
########################################################## 
           
def StoryDecision(transcript):
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

    #If the kid responds "strong warrior", gTTs matches, and the StrongWarrior file plays
    elif re.search("strong", transcript, re.I):
        SagaLights.Warrior()
        SagaServo.SagaOpens()
        CURR_STORY = StrongWarrior
        curr_fork = CURR_STORY.STORY_FORKS['Intro'] #this might need to change to be changing based on where it is (eg. i) 
        CURR_STORY.PlayCurrentFork(curr_fork)

    # #If the kid responds "clever", gTTs matches, and the CleverMagician file plays
    # elif re.search("clever", transcript, re.I):
    #     SagaLights.Magician()
    #     SagaServo.SagaOpens()
    #     CURR_STORY = CleverMagician
    #     curr_fork = CURR_STORY.STORY_FORKS['#####'] #this might need to change to be changing based on where it is (eg. i) 
    #     CURR_STORY.PlayCurrentFork(curr_fork)

    # #If the kid responds TODO : other stories 
    # elif re.search("oracle", transcript, re.I):
    #     SagaLights.#######NAME########()
    #     SagaServo.SagaOpens()
    #     CURR_STORY = CleverMagician
    #     curr_fork = CURR_STORY.STORY_FORKS['#####'] #this might need to change to be changing based on where it is (eg. i) 
    #     CURR_STORY.PlayCurrentFork(curr_fork)       
    

 def playAudio(text):
     text2Speech = gTTS(text, lang ='en')
     text2Speech.save('audioFile.mp3')
    
     pygame.mixer.init()
     pygame.mixer.music.load('audioFile.mp3')
     pygame.mixer.music.play()

#function for the capacitive touch which - when pressed - will offer the story choice and the gem stone will glow
def touch_to_start():
    crickit.touch_1.value
    print("Press the Capactive Touch button 1: touch_to_start()")
    if crickit.touch_1.value:
        SagaLights.SagaReady()
        time.sleep(1)
        print(crickit.touch_1.value)
    else:
        print("No button push detected.")
               

## ARE WE NO LONGER USING THIS AS WE'RE USING AUDIO FILES INSTEAD ???? ########
def playTextToAudio(text):
    #TODO: read in the text and play it as an audio file
    #google text to speech: check viviks example
    pass
    t2s = gTTS(text, lang ='en')
    t2s.save('Start.mp3')

######## SAGA'S MAIN WHICH SEQUENCES THE FUNCTIONALITY ##########
#################################################################

def Main():
    #Saga is closed to start 
    print("Saga is waiting")  
    SagaServo.SagaClosed()
    
    #initialize things 
    language_code = 'en-US'  # a BCP-47 language tag
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)
    
    # user touches the gem stone which triggers the book opening 
    touch_to_start() #this also triggers the gem stone to glow white
    print("Saga's capative touch and lights are working")
  
    #this section is where the action for the gTTs happens:
    ## SAGA OFFERS THE STORY CHOICES 
    playAudio('What kind of story do you want to hear tonight?')
    
    ##############################################################
    #if you get a response -> play the story 
    #if response == True  
        #play through the story 
    #if no response -> prompt "do you want to hear a story"
    

    ## SAGA LISTENS FOR THE INPUT AND THEN STARTS THE CORRESPONDING STORY ##### 
    ## the stories have a coloured gem stone associated which changes colour before Saga opens
    
    #mic set up to look for input and the info is sent to google for analysis 
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)
        ListenPrintLoop(responses)

   

if __name__ == '__main__':
    Main()
