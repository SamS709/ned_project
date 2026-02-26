import pygame
import os
import time

pygame.mixer.init()

pygame.mixer.music.load('Morpion/beep.wav')
pygame.mixer.music.play()

# Wait for the sound to finish playing
time.sleep(0.2)  # Adjust this to match your beep2.wav duration