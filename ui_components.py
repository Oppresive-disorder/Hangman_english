import os
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Optional
import pygame
import color_palette as cp
import tracker
import Hangman_monolith as HM
import Game_interface as GI
from words import get_definition, get_random_word
import math 


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1250, 720))
pygame.display.set_caption(" Hang Moni ")
CG_font = pygame.font.SysFont("Cormorant Garamond", 49)
CG_font_small = pygame.font.SysFont("Cormorant Garamond", 30)
pixel_font_path = os.path.join(os.path.dirname(__file__), "PixelifySans.ttf")
pixel_title_font = pygame.font.Font(pixel_font_path, 64)
pixel_button_font = pygame.font.Font(pixel_font_path, 27)
pixel_small_button_font = pygame.font.Font(pixel_font_path, 20)
pixel_display_font = pygame.font.Font(pixel_font_path, 22)
pixel_display_label_font = pygame.font.Font(pixel_font_path, 14)


def draw_background(surface):
    def __init__(self, x, y):
        hi = ()

def draw_pixel_text(surface, text, font, color, center, shadow_offset=(4, 4)):
    shadow = font.render(text, False, cp.deep_walnut)
    foreground = font.render(text, False, color)
    shadow_rect = shadow.get_rect(center=center).move(shadow_offset)
    surface.blit(shadow, shadow_rect)
    surface.blit(foreground, foreground.get_rect(center=center))

def draw_pixel_button(surface, rect, color, hovered=False, pressed=False):
    step = 6
    face_rect = rect.move(0, 4) if pressed else rect
    depth = 3 if pressed else 7

    if hovered:
        color = tuple(min(channel + 25, 255) for channel in color)

    def stepped_points(button_rect, y_offset=0):
        return [
            (button_rect.left + step, button_rect.top + y_offset),
            (button_rect.right - step, button_rect.top + y_offset),
            (button_rect.right - step, button_rect.top + y_offset + 3),
            (button_rect.right - 3, button_rect.top + y_offset + 3),
            (button_rect.right - 3, button_rect.top + y_offset + step),
            (button_rect.right, button_rect.top + y_offset + step),
            (button_rect.right, button_rect.bottom + y_offset - step),
            (button_rect.right - 3, button_rect.bottom + y_offset - step),
            (button_rect.right - 3, button_rect.bottom + y_offset - 3),
            (button_rect.right - step, button_rect.bottom + y_offset - 3),
            (button_rect.right - step, button_rect.bottom + y_offset),
            (button_rect.left + step, button_rect.bottom + y_offset),
            (button_rect.left + step, button_rect.bottom + y_offset - 3),
            (button_rect.left + 3, button_rect.bottom + y_offset - 3),
            (button_rect.left + 3, button_rect.bottom + y_offset - step),
            (button_rect.left, button_rect.bottom + y_offset - step),
            (button_rect.left, button_rect.top + y_offset + step),
            (button_rect.left + 3, button_rect.top + y_offset + step),
            (button_rect.left + 3, button_rect.top + y_offset + 3),
            (button_rect.left + step, button_rect.top + y_offset + 3),
        ]

    dark_color = tuple(max(channel - 55, 0) for channel in color)
    light_color = tuple(min(channel + 45, 255) for channel in color)
    pygame.draw.polygon(surface, dark_color, stepped_points(rect, depth))
    pygame.draw.polygon(surface, color, stepped_points(face_rect))
    pygame.draw.rect(
        surface,
        light_color,
        (face_rect.left + 8, face_rect.top + 7, face_rect.width - 16, 4),
    )
    pygame.draw.rect(
        surface,
        light_color,
        (face_rect.left + 7, face_rect.top + 8, 4, face_rect.height - 17),
    )


def draw_pixel_display(surface, rect, label, value, accent):
    pygame.draw.rect(surface, cp.sea_midnight, rect)
    pygame.draw.rect(surface, accent, rect, 2)
    pygame.draw.rect(surface, accent, (rect.left + 6, rect.top + 6, 4, 4))
    pygame.draw.rect(surface, accent, (rect.right - 10, rect.bottom - 10, 4, 4))

    label_surface = pixel_display_label_font.render(label.upper(), False, accent)
    value_surface = pixel_display_font.render(str(value), False, cp.ivory)
    surface.blit(label_surface, (rect.left + 14, rect.top + 5))
    surface.blit(
        value_surface,
        value_surface.get_rect(
            right=rect.right - 12,
            centery=rect.centery + 4,
        ),
    )


def draw_pixel_swing(surface, moni_img):
    anchor = pygame.Vector2(surface.get_width() // 2, 0)
    swing_angle = math.sin(pygame.time.get_ticks() / 1000) * math.radians(35)
    rope_length = 150
    swing_point = anchor + pygame.Vector2(
        math.sin(swing_angle) * rope_length,
        math.cos(swing_angle) * rope_length,
    )

    rotated_moni = pygame.transform.rotate(moni_img, -math.degrees(swing_angle))
    moni_center = swing_point + pygame.Vector2(
        math.sin(swing_angle) * moni_img.get_height() / 2,
        math.cos(swing_angle) * moni_img.get_height() / 2,
    )
    moni_rect = rotated_moni.get_rect(
        center=(round(moni_center.x), round(moni_center.y))
    )

    rope_vector = moni_center - anchor
    rope_length_pixels = round(rope_vector.length())
    rope_direction = rope_vector.normalize()
    for distance in range(0, rope_length_pixels, 8):
        pixel_position = anchor + rope_direction * distance
        pygame.draw.rect(
            surface,
            cp.deep_walnut,
            (round(pixel_position.x) - 2, round(pixel_position.y) - 2, 4, 4),
        )

    surface.blit(rotated_moni, moni_rect)


Easy_button = pygame.Rect(135, 600, 200, 50)
intermediate_button = pygame.Rect(395, 600, 200, 50)
hard_button = pygame.Rect(655, 600, 200, 50)
expert_button = pygame.Rect(915, 600, 200, 50)
welcome_text_string = "Welcome to Hang Moni"


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

    def draw(self, surface, mouse_pos, mouse_pressed):
        hovered = self.rect.collidepoint(mouse_pos)
        pressed = hovered and mouse_pressed
        draw_pixel_button(surface, self.rect, cp.mulberry_mist, hovered, pressed)
        label_center = self.rect.center
        if pressed:
            label_center = (self.rect.centerx, self.rect.centery + 4)
        draw_pixel_text(
            surface,
            "Home",
            pixel_button_font,
            cp.ivory,
            label_center,
            (1, 2) if pressed else (2, 3),
        )


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
        draw_pixel_display(surface, self.rect, "Moni", f"${value}", cp.mulberry_mist)


class streak_display:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 200, 50)


    def draw(self, surface, value):
        draw_pixel_display(surface, self.rect, "Streak", value, cp.blush_suede)
       
class highest_streak_display:    
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 200, 50)


    def draw(self, surface, value):
        draw_pixel_display(surface, self.rect, "Best streak", value, cp.blush_suede)


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
        self.font_size = 21
        self.scaled_sprites = {}


    def draw(self, surface, text, face_rect):
        screen_width, screen_height = surface.get_size()
        font = pygame.font.SysFont("Cormorant Garamond", self.font_size)
        horizontal_padding = 72
        vertical_padding = 56
        max_bubble_width = min(self.width + 40, screen_width - 16)
        widest_word = max(
            (font.size(word)[0] for word in text.split()),
            default=0,
        )
        bubble_width = max(
            min(self.width + 40, max_bubble_width),
            min(widest_word + horizontal_padding, max_bubble_width),
        )
        max_text_width = bubble_width - horizontal_padding

        def wrap_text(font):
            lines = []
            current_line = ""
            for word in text.split():
                pieces = []
                piece = ""
                for character in word:
                    if piece and font.size(piece + character)[0] > max_text_width:
                        pieces.append(piece)
                        piece = character
                    else:
                        piece += character
                if piece:
                    pieces.append(piece)

                for piece in pieces:
                    candidate = f"{current_line} {piece}".strip()
                    if current_line and font.size(candidate)[0] > max_text_width:
                        lines.append(current_line)
                        current_line = piece
                    else:
                        current_line = candidate
            if current_line:
                lines.append(current_line)
            return lines

        max_bubble_height = max(80, screen_height - 16)
        font_size = self.font_size
        lines = wrap_text(font)
        line_height = font.get_linesize()
        while (
            len(lines) * line_height + vertical_padding > max_bubble_height
            and font_size > 12
        ):
            font_size -= 1
            font = pygame.font.SysFont("Cormorant Garamond", font_size)
            lines = wrap_text(font)
            line_height = font.get_linesize()

        max_lines = max(1, (max_bubble_height - vertical_padding) // line_height)
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            last_line = lines[-1].rstrip(". ")
            while last_line and font.size(last_line + "...")[0] > max_text_width:
                last_line = last_line[:-1]
            lines[-1] = last_line + "..."

        bubble_height = min(
            max_bubble_height,
            max(self.height + 20, len(lines) * line_height + vertical_padding),
        )
        bubble_x = min(
            max(8, face_rect.right - 55),
            screen_width - bubble_width - 8,
        )
        bubble_y = min(
            max(8, face_rect.top - bubble_height + 35),
            screen_height - bubble_height - 8,
        )
        rect = pygame.Rect(
            bubble_x,
            bubble_y,
            bubble_width,
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
            text_surface = font.render(line, True, cp.black)
            surface.blit(
                text_surface,
                text_surface.get_rect(centerx=rect.centerx, top=text_y),
            )
            text_y += line_height


buttons = [
    (Easy_button, cp.terracotta_dust, "Easy"),
    (intermediate_button, cp.baked_earth, "Intermediate"),
    (hard_button, cp.vintage_rose, "Hard"),
    (expert_button, cp.slate_navy, "Expert"),
]


moni_box = moni_display(1000, 50)
streak_box = streak_display(1000, 110)
highest_streak_box = highest_streak_display(1000, 170)
home_button = Home_Button(30, 30)
game_platform = platform(0, 45, 675, 675)
moni_face = Moni_face(535, 110)
moni_speech_bubble = speech_bubble(0, 0, 300, 140)
definition_executor = ThreadPoolExecutor(max_workers=1)
word_future: Optional[Future[str]] = None
definition_future: Optional[Future[str]] = None
current_screen = "menu"
current_level = None


game_word = ""
game_definition = ""
definition_error = ""
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
                tracker.set_level(current_level)
                current_screen = "game"
                game_word = ""
                guessed_letters.clear()
                game_over = False
                round_result = ""
                guess_message = ""
                word_future = definition_executor.submit(
                    get_random_word, current_level
                )
            elif current_screen == "game" and home_button.rect.collidepoint(event.pos):
                current_screen = "menu"
        elif current_screen == "game" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                current_screen = "menu"
            elif game_over and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                tracker.reset_round()
                game_word = ""
                game_definition = ""
                definition_error = ""
                guessed_letters.clear()
                game_over = False
                round_result = ""
                guess_message = ""
                word_future = definition_executor.submit(
                    get_random_word, current_level
                )
            elif (
                word_future is None
                and not game_over
                and len(event.unicode) == 1
                and event.unicode.isalpha()
            ):
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

    if word_future is not None and word_future.done():
        selected_word = word_future.result().lower()
        word_future = None
        if current_screen == "game":
            game_word = selected_word
            game_definition = ""
            definition_error = ""
            definition_future = definition_executor.submit(
                get_definition, game_word
            )

    if definition_future is not None and definition_future.done():
        try:
            game_definition = definition_future.result()
        except Exception as error:
            definition_error = str(error)
            print(f"Definition lookup failed: {error}")
        definition_future = None

    delta_time = clock.tick(60) / 1000
    cat.update(delta_time)
    screen.fill(cp.ivory)


    if current_screen == "menu":
        moni_box.draw(screen, tracker.moni)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        for button, color, label in buttons:
            hovered = button.collidepoint(mouse_pos)
            pressed = hovered and mouse_pressed
            draw_pixel_button(screen, button, color, hovered, pressed)
            label_font = (
                pixel_small_button_font
                if label == "Intermediate"
                else pixel_button_font
            )
            label_center = button.center
            if pressed:
                label_center = (button.centerx, button.centery + 4)
            draw_pixel_text(
                screen,
                label,
                label_font,
                cp.ivory,
                label_center,
                (1, 2) if pressed else (2, 3),
            )
        draw_pixel_swing(screen, cat.frames[cat.frame_index])
        draw_pixel_text(
            screen,
            welcome_text_string,
            pixel_title_font,
            cp.spiced_wine,
            (screen.get_width() // 2, 100),
        )
    else:
        home_button.draw(
            screen, pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]
        )
        game_platform.draw(screen)
        face_rect = moni_face.draw(
            screen, tracker.wrong_guesses, tracker.max_guesses
        )
        if game_over:
            if definition_error:
                bubble_text = f"Definition lookup failed: {definition_error}"
            elif game_definition:
                bubble_text = f"Definition: {game_definition}"
            else:
                bubble_text = "Looking up definition..."
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
                "Enter to Continue", True, cp.spiced_wine
            )
            screen.blit(restart_text, restart_text.get_rect(center=(930, 580)))
        else:
            instruction = CG_font_small.render(
                "Type a letter to guess", True, cp.spiced_wine
            )
            screen.blit(instruction, instruction.get_rect(center=(930, 530)))


    pygame.display.flip()
pygame.quit()
