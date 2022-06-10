from unittest import TestCase
import json
from boggle import BoggleGame

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- Boggle homepage testing -->', html)


    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post("/api/new-game")
            response_str = response.get_data(as_text=True)
            response_json = json.loads(response_str)
            self.assertEqual(response.status_code, 200)
            self.assertIn("gameId", response_json)
            self.assertIn("board", response_json)
            self.assertEqual(type(response_json["board"]), list)
            self.assertEqual(type(response_json["board"][0]), list)
            self.assertEqual(type(response_json["board"][1]), list)
            self.assertEqual(type(response_json["board"][2]), list)
            self.assertEqual(type(response_json["board"][3]), list)
            self.assertEqual(type(response_json["board"][4]), list)
            self.assertIn(response_json["gameId"], games)

    def test_score_word(self):
        """Test scoring a word """

        with self.client as client:
            games["1"] = BoggleGame()
            games["1"].board = [['C', 'A', 'T', 'T', 'T'],
                            ['C', 'A', 'T', 'T', 'T'],
                            ['C', 'A', 'T', 'T', 'T'],
                            ['C', 'A', 'T', 'T', 'T'],
                            ['C', 'A', 'T', 'T', 'T']]

            response = client.post("/api/score-word", json= {"gameId":"1", 
                                    "word":"CAT"})
            response_json = response.get_json()
            self.assertEqual(response_json['result'], 'ok')

            response = client.post(
                "/api/score-word", json={"gameId": "1", "word": "TTT"})
            response_json = response.get_json()
            self.assertEqual(response_json['result'], 'not-word')

            response = client.post(
                "/api/score-word", json={"gameId": "1", "word": "BAT"})
            response_json = response.get_json()
            self.assertEqual(response_json['result'], 'not-on-board')
