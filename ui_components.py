import pygame 
import Hangman_monolith

pygame.init()

screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Start Moni")

clock = pygame.time.Clock()
running = True 

while running:

    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False

screen.fill("MONI")
