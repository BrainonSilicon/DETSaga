from gtts import gTTS
import pygame 


def playAudio(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

if __name__ == '__main__':
    pass