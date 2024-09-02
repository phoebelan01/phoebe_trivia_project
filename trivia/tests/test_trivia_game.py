from unittest import mock
from django.test import TestCase
from trivia.game_logic.trivia_game import start_game

class TriviaGameTest(TestCase):

    @mock.patch('trivia.game_logic.trivia_game.generate_trivia_questions')
    @mock.patch('builtins.input', side_effect=[4, 4, 4, 4, 4, 4, 4, 4, 4, 4])  # Mocking input to always return '4'
    def test_trivia_game(self, mock_input, mock_generate):
        # Mock the generate_trivia_questions function
        mock_generate.return_value = [
            {
                "theme": "Science",
                "question": "What is the largest planet in our solar system?",
                "options": ["Mars", "Earth", "Saturn", "Jupiter"],
                "answer": 4
            }
        ] * 10  # Return 10 identical questions
 
        api_key = "your-api-key"
        theme = "Science"
        num_players = 2
        player_names = ["Phoebe", "Bob"]
 
        # Run the game without expecting any interaction
        start_game(api_key, theme, num_players, player_names)
 
        # You can add assertions here to verify the game logic,
        # for example, checking that the mock was called the expected number of times.
        self.assertEqual(mock_input.call_count, 10)