import pygame
import os
import time

pygame.mixer.init()
pygame.mixer.music.load('Connect4/beep.mp3')
pygame.mixer.music.play()

# Wait for the sound to finish playing
time.sleep(1)  # Adjust this to match your beep2.wav duration