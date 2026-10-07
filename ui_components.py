import os
import pygame
import color_palette as cp
import tracker
import Hangman_monolith as HM
import Game_interface as GI
from words import get_definition, get_random_word




pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1250, 720))
pygame.display.set_caption(" Hang Moni ")
CG_font = pygame.font.SysFont("Cormorant Garamond", 49)
CG_font_small = pygame.font.SysFont("Cormorant Garamond", 30)


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


class Home_Button:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 50)
        self.text = CG_font_small.render("Home", True, cp.ivory)


    def draw(self, surface):
        pygame.draw.rect(surface, cp.mulberry_mist, self.rect)
        surface.blit(self.text, self.text.get_rect(center=self.rect.center))


class platform:
    def __init__(self, x, y, width, height):
        sprite = pygame.image.load(os.path.join(os.path.dirname(__file__), "platform.png")).convert_alpha()
        self.rect = pygame.Rect(x, y, width, height)
        self.sprite = pygame.transform.scale(sprite, (width, height))
        width, height = self.rect.size


    def draw(self, surface):
        surface.blit(self.sprite, self.rect)




       
class moni_display:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 200, 50)


    def draw(self, surface, value):
        pygame.draw.rect(surface, cp.mulberry_mist, self.rect)
        text = CG_font_small.render(f"Moni: ${value}", True, cp.ivory)
        surface.blit(text, text.get_rect(center=self.rect.center))


class streak_display:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 200, 50)


    def draw(self, surface, value):
        pygame.draw.rect(surface, cp.blush_suede, self.rect)
        text = CG_font_small.render(f"Streak: {value}", True, cp.ivory)
        surface.blit(text, text.get_rect(center=self.rect.center))
       
class highest_streak_display:    
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 200, 50)


    def draw(self, surface, value):
        pygame.draw.rect(surface, cp.blush_suede, self.rect)
        text = CG_font_small.render(f"Best streak: {value}", True, cp.ivory)
        surface.blit(text, text.get_rect(center=self.rect.center))


class Moni_face:
    def __init__(self, x, y):
        self.x = x
        self.start_y = y
        self.sprite1 = pygame.image.load(os.path.join(os.path.dirname(__file__), "1 smile.png"))
        self.sprite2 = pygame.image.load(os.path.join(os.path.dirname(__file__), "2 eye google.png"))
        self.sprite3 = pygame.image.load(os.path.join(os.path.dirname(__file__), "3 face_down.png"))
        self.sprite4 = pygame.image.load(os.path.join(os.path.dirname(__file__), "4 close eye jig.png"))
        self.sprite5 = pygame.image.load(os.path.join(os.path.dirname(__file__), "5 steal from Riho.png"))
        self.sprite6 = pygame.image.load(os.path.join(os.path.dirname(__file__), "6 tounge out.png"))
        self.sprite7 = pygame.image.load(os.path.join(os.path.dirname(__file__), "7 anger.png"))


        self.sprites = (
            self.sprite1,
            self.sprite2,
            self.sprite3,
            self.sprite4,
            self.sprite5,
            self.sprite6,
            self.sprite7,
        )


    def draw(self, surface, wrong_guesses, max_guesses):
        last_y = surface.get_height() - self.sprites[0].get_height()
        travel_distance = max(0, last_y - self.start_y)
        progress = min(max(wrong_guesses, 0), max_guesses)
        y = self.start_y + travel_distance * progress / max_guesses
        expression_index = round(
            (len(self.sprites) - 1) * progress / max_guesses
        )
        face = self.sprites[expression_index]
        face_rect = surface.blit(face, (self.x, round(y)))
        return face_rect


class speech_bubble:
    def __init__(self, x, y, width, height):
        sprite = pygame.image.load(
            os.path.join(os.path.dirname(__file__), "speach bubble.png")
        ).convert_alpha()
        self.x = x
        self.width = width
        self.height = height
        self.sprite = sprite
        self.font = pygame.font.SysFont("Cormorant Garamond", 21)
        self.scaled_sprites = {}


    def draw(self, surface, text, face_rect):
        max_text_width = self.width - 56
        lines = []
        line = ""
        for word in text.split():
            candidate = f"{line} {word}".strip()
            if line and self.font.size(candidate)[0] > max_text_width:
                lines.append(line)
                line = word
            else:
                line = candidate
        if line:
            lines.append(line)


        line_height = self.font.get_linesize()
        bubble_height = max(self.height, len(lines) * line_height + 40)
        rect = pygame.Rect(
            face_rect.right - 55,
            max(0, face_rect.top - bubble_height + 35),
            self.width,
            bubble_height,
        )
        if rect.size not in self.scaled_sprites:
            self.scaled_sprites[rect.size] = pygame.transform.scale(
                self.sprite, rect.size
            )
        bubble_sprite = self.scaled_sprites[rect.size]
        surface.blit(bubble_sprite, rect)


        text_y = rect.centery - len(lines) * line_height // 2
        for line in lines:
            text_surface = self.font.render(line, True, cp.black)
            surface.blit(
                text_surface,
                text_surface.get_rect(centerx=rect.centerx, top=text_y),
            )
            text_y += line_height


buttons = [
    (Easy_button, cp.terracotta_dust, CG_font.render("Easy", True, cp.ivory)),
    (intermediate_button, cp.baked_earth, CG_font_small.render("Intermediate", True, cp.ivory)),
    (hard_button, cp.vintage_rose, CG_font.render("Hard", True, cp.ivory)),
    (expert_button, cp.slate_navy, CG_font.render("Expert", True, cp.ivory)),
]


moni_box = moni_display(1000, 50)
streak_box = streak_display(1000, 110)
highest_streak_box = highest_streak_display(1000, 170)
home_button = Home_Button(30, 30)
game_platform = platform(0, 45, 675, 675)
moni_face = Moni_face(505, 110)
moni_speech_bubble = speech_bubble(0, 0, 300, 140)
current_screen = "menu"
current_level = None


game_word = ""
game_definition = ""
guessed_letters = set()
game_over = False
round_result = ""
guess_message = ""


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
            level_selection = next(
                (
                    (name, level)
                    for button, name, level in (
                        (Easy_button, "Easy", 1),
                        (intermediate_button, "Intermediate", 2),
                        (hard_button, "Hard", 3),
                        (expert_button, "Expert", 4),
                    )
                    if button == clicked_button
                ),
                None,
            )
            if level_selection is not None and current_screen == "menu":
                _, current_level = level_selection
                current_screen = "game"
                tracker.set_level(current_level)
                game_word = get_random_word(current_level).lower()
                game_definition = get_definition(game_word)
                guessed_letters.clear()
                game_over = False
                round_result = ""
                guess_message = ""
            elif current_screen == "game" and home_button.rect.collidepoint(event.pos):
                current_screen = "menu"
        elif current_screen == "game" and event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                tracker.reset_round()
                game_word = get_random_word(current_level).lower()
                game_definition = get_definition(game_word)
                guessed_letters.clear()
                game_over = False
                round_result = ""
                guess_message = ""
            elif not game_over and len(event.unicode) == 1 and event.unicode.isalpha():
                letter = event.unicode.lower()
                if letter in guessed_letters:
                    guess_message = f"Already guessed {letter}"
                else:
                    guess_message = ""
                    guessed_letters.add(letter)
                    if letter not in game_word:
                        tracker.add_wrong_guess()


                    won = tracker.is_word_complete(game_word, guessed_letters)
                    lost = tracker.is_max_guesses_reached()
                    if won or lost:
                        game_over = True
                        round_result = "You win!" if won else f"You lose! The word was {game_word}."
                        tracker.update_streak(won)


    if not running:
        break


    delta_time = clock.tick(60) / 1000
    cat.update(delta_time)
    screen.fill(cp.ivory)


    if current_screen == "menu":
        moni_box.draw(screen, tracker.moni)
        for button, color, label in buttons:
            pygame.draw.rect(screen, color, button)
            screen.blit(label, label.get_rect(center=button.center))
        cat.draw(screen)
        screen.blit(
            welcome_text,
            welcome_text.get_rect(center=(screen.get_width() // 2, 100)),
        )
    else:
        home_button.draw(screen)
        game_platform.draw(screen)
        face_rect = moni_face.draw(
            screen, tracker.wrong_guesses, tracker.max_guesses
        )
        if game_over:
            bubble_text = f"Definition: {game_definition}"
        elif guess_message:
            bubble_text = guess_message
        else:
            bubble_text = "Keep going!"
        moni_speech_bubble.draw(screen, bubble_text, face_rect)
        moni_box.draw(screen, tracker.moni)
        streak_box.draw(screen, tracker.streak)
        highest_streak_box.draw(screen, tracker.highest_streak)
        shown_word = tracker.get_display_word(game_word, guessed_letters)
        word_text = CG_font.render(shown_word, True, cp.spiced_wine)
        screen.blit(word_text, word_text.get_rect(center=(930, 400)))
        guesses_text = CG_font_small.render(
            f"Wrong guesses: {tracker.wrong_guesses}/{tracker.max_guesses}",
            True,
            cp.spiced_wine,
        )
        screen.blit(guesses_text, guesses_text.get_rect(center=(930, 470)))
        if round_result:
            result_text = CG_font_small.render(round_result, True, cp.spiced_wine)
            screen.blit(result_text, result_text.get_rect(center=(930, 530)))
            restart_text = CG_font_small.render(
                "Press R to continue", True, cp.spiced_wine
            )
            screen.blit(restart_text, restart_text.get_rect(center=(930, 580)))
        else:
            instruction = CG_font_small.render(
                "Type a letter to guess", True, cp.spiced_wine
            )
            screen.blit(instruction, instruction.get_rect(center=(930, 530)))


    pygame.display.flip()
pygame.quit()



