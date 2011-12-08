"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
#stuff added by programmer is below:
from django.utils import unittest
from player.models import Player
from datetime import datetime



question="Do you like "+ "test_file" +" ?"
pub_date=datetime.now()
file_name="test_file"
frame_num_start=0
frame_num_stop=0
 
class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(question=question,  pub_date=pub_date,  file_name=file_name, frame_num_start=frame_num_start, frame_num_stop=frame_num_stop)
    def testAttrib(self):
        self.assertEqual(self.player1.question, question)
        self.assertEqual(self.player1.pub_date, pub_date)
        self.assertEqual(self.player1.file_name, file_name)
        self.assertEqual(self.player1.frame_num_start, frame_num_start)
        self.assertEqual(self.player1.frame_num_stop, frame_num_stop)


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
