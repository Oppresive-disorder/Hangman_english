import unittest
from unittest.mock import patch

import tracker
import Game_interface


class GameInterfaceTests(unittest.TestCase):
    def test_mono_game_sets_selected_level(self):
        tracker.level1 = False
        tracker.level2 = False
        tracker.level3 = False
        tracker.level4 = False
        tracker.wrong_guesses = 3
        tracker.max_guesses = 6

        with patch("builtins.input", return_value="2"), patch("Game_interface.play_game") as mock_play:
            Game_interface.mono_game()

        self.assertTrue(tracker.level2)
        self.assertEqual(tracker.max_guesses, 6)
        self.assertEqual(tracker.wrong_guesses, 0)
        mock_play.assert_called_once_with(2)


if __name__ == "__main__":
    unittest.main()
