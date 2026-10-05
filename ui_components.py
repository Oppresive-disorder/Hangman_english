import pygame 
import Hangman_monolith
import Game_interface

screen = pygame.display.set_mode((1250, 720))
pygame.display.set_caption(" Hang Moni ")

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((234, 218, 171))
    pygame.display.flip()
    clock.tick(60)

    game_interface = Game_interface.GameInterface(screen)
    Hangman_monolith = Hangman_monolith.HangmanMonolith(screen, game_interface)



