from tracker import (
    add_wrong_guess,
    get_display_word,
    is_max_guesses_reached,
    is_word_complete,
    reset_round,
    set_level,
    update_streak,
)
import tracker
from words import get_definition, get_random_word



def word_grab(level_num):
    word = get_random_word(level_num).lower()
    definition = get_definition(word)
    return word, definition


def core_gameplayloop(word, definition): 
    guessed_letters = []

    print(f"Let's play hangman! [{get_display_word(word, guessed_letters)}]")

    while not is_word_complete(word, guessed_letters) and not is_max_guesses_reached():
        user_guess = input("Guess a letter >> ").strip().lower()

        if len(user_guess) != 1 or not user_guess.isalpha():
            print("Please enter one letter.")
            continue
        if user_guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.append(user_guess)

        if user_guess in word:
            print("Correct!")
        else:
            add_wrong_guess()
            print(f"Wrong! Misses left: {tracker.max_guesses - tracker.wrong_guesses}")

        print(f"[{get_display_word(word, guessed_letters)}]")

   
    won = is_word_complete(word, guessed_letters)
    update_streak(won)

    print("\nYou win!" if won else f"\nYou lose! The word was {word}.")
    print("---------------------------------")
    print("Definition:", definition) 
    print(f"Streak: {tracker.streak} | Moni: ${tracker.moni}")


if __name__ == "__main__":
    level_num = 1  


    set_level(level_num)
    reset_round()

    word, definition = word_grab(level_num)
    core_gameplayloop(word, definition) 