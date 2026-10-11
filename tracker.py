streak = 0
moni = 10
highest_streak = 0

level1 = False
level2 = False
level3 = False
level4 = False

wrong_guesses = 0
max_guesses = 6


def get_display_word(chosen_word, guessed_letters):
    display_list = []
    for letter in chosen_word:
        if letter in guessed_letters:
            display_list.append(letter)
        else:
            display_list.append("_")

    return " ".join(display_list)


def is_word_complete(chosen_word, guessed_letters):
    for letter in chosen_word:
        if letter not in guessed_letters:
            return False
    return True


def set_level(level_num):
    global level1, level2, level3, level4, max_guesses

    level1 = level_num == 1
    level2 = level_num == 2
    level3 = level_num == 3
    level4 = level_num == 4

    if level1:
        max_guesses = 7
    elif level2:
        max_guesses = 8
    elif level3:
        max_guesses = 9
    elif level4:
        max_guesses = 10

    reset_round()


def add_wrong_guess():
    global wrong_guesses
    wrong_guesses += 1


def is_max_guesses_reached():
    return wrong_guesses >= max_guesses


def reset_round():
    global wrong_guesses
    wrong_guesses = 0


def update_streak(Correct):
    global streak, moni, highest_streak

    if Correct:
        streak += 1
        if streak > highest_streak:
            highest_streak = streak

        if level1:
            moni += 3
        elif level2:
            moni += 5
        elif level3:
            moni += 6
        elif level4:
            moni += 8
    else:
        streak = 0