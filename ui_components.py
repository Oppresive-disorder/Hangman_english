import pygame 
import Hangman_monolith
import Game_interface

screen = pygame.display.set_mode((1250, 720))
pygame.display.set_caption("Start Moni")

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((234, 218, 171))
    pygame.display.flip()
    clock.tick(60)
