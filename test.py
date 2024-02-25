from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json


class FlaskTests(TestCase):
    """Unit tests for Boggle app."""

    def test_display_board(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Boggle</h1>', html)

    def test_update_stats(self):
        with app.test_client() as client:
                with client.session_transaction() as change_session:
                    change_session['visited'] = 12
                    change_session['highest_score'] = 10
                resp = client.post('/game-over', json={'score': 3})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(session['visited'], 13)               
                self.assertEqual(session['highest_score'], 10)

    def test_game_over(self):
        with app.test_client() as client:
                with client.session_transaction() as change_session:
                    change_session['highest_score'] = 100               
                resp = client.post('/game-over', json={'score': 3})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.get_json(),{'highest_score': 100})


    def test_verify(self):
        boggle_game = Boggle()
        board = boggle_game.make_board()        
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                    change_session['board'] = board
            resp = client.post('/verify', json={'guess': 'alefj'})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(),{'result': 'not-word'})

    def test_dupes(self):
        boggle_game = Boggle()
        board = boggle_game.make_board()        
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                    change_session['board'] = board
            resp = client.post('/verify', json={'guess': 'word'})
            resp = client.post('/verify', json={'guess': 'word'})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(),{'result': 'already-submitted-word'})        
            