import unittest
from unittest.mock import MagicMock, patch
import pygame


import Shaolin_Harmony_Heavens_Slots
from Shaolin_Harmony_Heavens_Slots import (
    spin_reels,
    check_winning_conditions,
    play_background_theme,
    stop_background_theme,
)


class TestSlotMachine(unittest.TestCase):

    def test_spin_reels(self):
        result_reels = spin_reels()
        self.assertEqual(len(result_reels), 9)


    def test_check_winning_conditions(self):
        result_reels = ["monk"] * 9
        bet_amount = 10.00
        self.assertTrue(check_winning_conditions(result_reels, bet_amount))

        result_reels = ["temple"] * 9
        bet_amount = 5.00
        self.assertTrue(check_winning_conditions(result_reels, bet_amount))

    @patch('pygame.mixer.music')
    def test_play_background_theme(self, mock_music):
        play_background_theme()
        mock_music.load.assert_called_once_with("sounds/china_song.mp3")
        mock_music.set_volume.assert_called_once_with(0.1)
        mock_music.play.assert_called_once_with(-1)

    @patch('pygame.mixer.music')
    def test_stop_background_theme(self, mock_music):
        stop_background_theme()
        mock_music.stop.assert_called_once()

    def test_spin_reels_with_mocked_random_choice(self):
        with patch('random.choice', return_value="monk"):
            result_reels = spin_reels()
        self.assertEqual(result_reels, ["monk"] * 9)

    def test_check_winning_conditions_no_win(self):
        result_reels = ["monk", "temple", "power", "meditate", "letter", "dragon", "shuriken", "monk", "temple"]
        bet_amount = 10.00
        self.assertFalse(check_winning_conditions(result_reels, bet_amount))

    def test_spin_reels_with_different_symbols(self):
        with patch('random.choice',
                   side_effect=["monk", "temple", "power", "meditate", "letter", "dragon", "shuriken"] * 2):
            result_reels = spin_reels()
        self.assertEqual(len(result_reels), 9)
        self.assertEqual(len(set(result_reels)), 9)

    def test_check_winning_conditions_no_balance(self):
        result_reels = ["monk"] * 9
        bet_amount = 100.00
        self.assertFalse(check_winning_conditions(result_reels, bet_amount))

    def test_check_winning_conditions_max_balance_win(self):
        result_reels = ["monk"] * 9
        bet_amount = 10.00
        balance = 100000.00
        with patch('your_main_file_name.balance', return_value=balance):
            self.assertTrue(check_winning_conditions(result_reels, bet_amount))

    def test_bet_buttons(self):
        with patch('Shaolin_Harmony_Heavens_Slots.display_result') as mock_display_result:
            with patch('Shaolin_Harmony_Heavens_Slots.check_winning_conditions', return_value=False):
                with patch('builtins.print') as mock_print:
                    with patch('Shaolin_Harmony_Heavens_Slots.sounds_dict["win"].play'):
                        with patch('Shaolin_Harmony_Heavens_Slots.shake_winning_icons'):
                            with patch('Shaolin_Harmony_Heavens_Slots.balance', return_value=100.00):
                                with patch('Shaolin_Harmony_Heavens_Slots.winnings', return_value=0.00):
                                    with patch('Shaolin_Harmony_Heavens_Slots.reels', return_value=["monk"] * 9):
                                        with patch('Shaolin_Harmony_Heavens_Slots.balance', return_value=100.00):
                                            for button_index, button in enumerate(
                                                    Shaolin_Harmony_Heavens_Slots.bet_buttons):
                                                bet_button_event = MagicMock()
                                                bet_button_event.type = pygame.MOUSEBUTTONDOWN
                                                bet_button_event.pos = (button["rect"].x + 10, button["rect"].y + 5)
                                                pygame.event.get.return_value = [bet_button_event]
                                                self.assertEqual(mock_display_result.call_count, 0)
                                                self.assertEqual(mock_print.call_count, 0)
                                                self.assertEqual(mock_display_result.call_count, 0)
                                                self.assertEqual(mock_print.call_count, 0)
                                                self.assertEqual(mock_display_result.call_count, 0)



    def test_deposit_button(self):

        with patch('builtins.print') as mock_print:
            with patch('Shaolin_Harmony_Heavens_Slots.sounds_dict["cashier"].play') as mock_cashier_sound:
                deposit_button_event = MagicMock()
                deposit_button_event.type = pygame.MOUSEBUTTONDOWN
                deposit_button_event.pos = (Shaolin_Harmony_Heavens_Slots.deposit_button_rect.x + 10,
                                            Shaolin_Harmony_Heavens_Slots.deposit_button_rect.y + 5)
                pygame.event.get.return_value = [deposit_button_event]
                self.assertEqual(mock_print.call_count, 0)
                self.assertEqual(mock_cashier_sound.call_count, 1)
                self.assertEqual(Shaolin_Harmony_Heavens_Slots.balance, 0)


if __name__ == '__main__':
    unittest.main()
