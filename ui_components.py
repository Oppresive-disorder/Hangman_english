import pygame 
import Hangman_monolith

screen = pygame.display.set_mode(800,600)
pygame.display.set_caption("Start Moni")

clock = pygame.time.Clock()

running = True


for event in pygame.event.get():
    if running:

         if event.type == pygame.QUIT:
            running = False
