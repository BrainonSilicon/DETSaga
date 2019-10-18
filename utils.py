from gtts import gTTS
import pygame 


 def playAudio(text):
     text2Speech = gTTS(text, lang ='en')
     text2Speech.save('audioFile.mp3')
    
     pygame.mixer.init()
     pygame.mixer.music.load('audioFile.mp3')
     pygame.mixer.music.play()