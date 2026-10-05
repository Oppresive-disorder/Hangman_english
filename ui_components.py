import pygame
import Hangman_monolith
import tracker
import color_palette as cp

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1250, 720))
pygame.display.set_caption(" Hang Moni ")
CG_font = pygame.font.SysFont("Cormorant Garamond", 49)
CG_font_small = pygame.font.SysFont("Cormorant Garamond", 30)

Easy_button = pygame.Rect(150, 335, 200, 50)
intermediate_button = pygame.Rect(400, 335, 200, 50)
hard_button = pygame.Rect(650, 335, 200, 50)
expert_button = pygame.Rect(900, 335, 200, 50)
buttons = [
    (Easy_button, cp.terracotta_dust, CG_font_small.render("Easy", True, cp.ivory)),
    (intermediate_button, cp.baked_earth, CG_font_small.render("Intermediate", True, cp.ivory)),
    (hard_button, cp.vintage_rose, CG_font_small.render("Hard", True, cp.ivory)),
    (expert_button, cp.slate_navy, CG_font_small.render("Expert", True, cp.ivory)),
]

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(cp.ivory)
    for button, color, label in buttons:
        pygame.draw.rect(screen, color, button)
        screen.blit(label, label.get_rect(center=button.center))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()



