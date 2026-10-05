from turtle import color

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
pygame.quit()            

pastel_cream = (255, 253, 208)
while True:
    screen.fill(pastel_cream)
    pygame.display.flip() 