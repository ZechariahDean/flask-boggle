from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """setup before each test"""
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_home(self):
        """check all html for home page"""

        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Time Left:', res.data)
            self.assertIn(b'High Score:', res.data)
            self.assertIn(b'You have played', res.data)
            self.assertEqual(session.get('h_score'), None)
            self.assertEqual(session.get('num_plays'), None)
    
    def test_validity(self):
        """check words for validity"""
        with self.client as client:
            client.get('/')
            with client.session_transaction() as session:
                session["board"] = [['T', 'A', 'B', 'L', 'E'],
                                    ['F', 'O', 'R', 'C', 'E'],
                                    ['B', 'R', 'A', 'I', 'N'],
                                    ['D', 'A', 'N', 'C', 'E'],
                                    ['K', 'N', 'I', 'H', 'T']]
            

            table = client.get('/check?word=table')
            oracle = client.get('/check?word=oracle')
            ten = client.get('/check?word=ten')
            bar = client.get('/check?word=bar')
            think = client.get('/check?word=think')

            self.assertEqual(table.json['result'], 'ok')
            self.assertEqual(oracle.json['result'], 'ok')
            self.assertEqual(ten.json['result'], 'ok')
            self.assertEqual(bar.json['result'], 'ok')
            self.assertEqual(think.json['result'], 'ok')

    def test_in_dictionary(self):
        """test if dictionary contains word"""
        
        self.client.get('/')
        res = self.client.get('/check?word=thisisnotasingleword')
        self.assertEqual(res.json['result'], 'not-word')

    def test_on_board(self):
        """check if word not in dictionary"""

        self.client.get('/')
        res = self.client.get('/check?word=incendiary')
        self.assertEqual(res.json['result'], 'not-on-board')