from unittest import TestCase
import json

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""
        games = {}
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
