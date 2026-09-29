import tracker
from Hangman_monolith import play_game


def mono_game():
    print(" >>welcome to hang Moni <><-><> ")
    print(" Chose dificulty ")

    while True:
        user_input = input(" <1,2,3,4> ").strip()
        if user_input in {"1", "2", "3", "4"}:
            level_num = int(user_input)
            tracker.set_level(level_num)
            tracker.reset_round()
            play_game(level_num)
            return
        print("Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    mono_game()
