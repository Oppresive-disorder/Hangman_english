import os
import pygame
import color_palette as cp
import Hangman_monolith as HM
import Game_interface as GI 


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1250, 720))
pygame.display.set_caption(" Hang Moni ")
CG_font = pygame.font.SysFont("Cormorant Garamond", 49)
CG_font_small = pygame.font.SysFont("Cormorant Garamond", 30)

<<<<<<< HEAD
Easy_button = pygame.Rect(150, 335, 200, 50)
intermediate_button = pygame.Rect(400, 335, 200, 50)
hard_button = pygame.Rect(650, 335, 200, 50)
expert_button = pygame.Rect(900, 335, 200, 50)
buttons = [
    (Easy_button, cp.terracotta_dust, CG_font_small.render("Easy", True, cp.ivory)),
    (intermediate_button, cp.baked_earth, CG_font_small.render("Intermediate", True, cp.ivory)),
    (hard_button, cp.vintage_rose, CG_font_small.render("Hard", True, cp.ivory)),
    (expert_button, cp.slate_navy, CG_font_small.render("Expert", True, cp.ivory)),
=======
Easy_button = pygame.Rect(135, 600, 200, 50)
intermediate_button = pygame.Rect(395, 600, 200, 50)
hard_button = pygame.Rect(655, 600, 200, 50)
expert_button = pygame.Rect(915, 600, 200, 50)
welcome_text_string = "Welcome to Hang Moni"
welcome_font = pygame.font.SysFont("Cormorant Garamond", 80)
welcome_text = welcome_font.render(welcome_text_string, True, cp.spiced_wine)

class AnimatedCat:
    def __init__(self, x, y):
        sprite_sheet_path = os.path.join(os.path.dirname(__file__), "cat_animation-Sheet.png")
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        frame_size = 128
        frame_count = sprite_sheet.get_width() // frame_size
        self.frames = [
            pygame.transform.scale(
                sprite_sheet.subsurface((i * frame_size, 0, frame_size, frame_size)),
                (392, 392),
            )
            for i in range(frame_count)
        ]
        self.rect = self.frames[0].get_rect(center=(x, y))
        self.frame_index = 0
        self.animation_timer = 0

    def update(self, delta_time):
        self.animation_timer += delta_time
        while self.animation_timer >= 0.1:
            self.animation_timer -= 0.1
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw(self, surface):
        surface.blit(self.frames[self.frame_index], self.rect)


cat = AnimatedCat(screen.get_width() // 2, 360)

buttons = [
    (Easy_button, cp.terracotta_dust, CG_font.render("Easy", True, cp.ivory)),
    (intermediate_button, cp.baked_earth, CG_font_small.render("Intermediate", True, cp.ivory)),
    (hard_button, cp.vintage_rose, CG_font.render("Hard", True, cp.ivory)),
    (expert_button, cp.slate_navy, CG_font.render("Expert", True, cp.ivory)),
>>>>>>> 908ed11ca68057989cf422c1435487643df90107
]

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_button = next(
                (button for button, _, _ in buttons if button.collidepoint(event.pos)),
                None,
            )
            if clicked_button == Easy_button:
                HM.play_game(1)
            elif clicked_button == intermediate_button:
                HM.play_game(2)
            elif clicked_button == hard_button:
                HM.play_game(3)
            elif clicked_button == expert_button:
                HM.play_game(4)

    if not running:
        break

    delta_time = clock.tick(60) / 1000
    cat.update(delta_time)
    screen.fill(cp.ivory)
    for button, color, label in buttons:
        pygame.draw.rect(screen, color, button)
        screen.blit(label, label.get_rect(center=button.center))
    cat.draw(screen)
    screen.blit(welcome_text, welcome_text.get_rect(center=(screen.get_width() // 2, 100)))
    pygame.display.flip()
pygame.quit()
