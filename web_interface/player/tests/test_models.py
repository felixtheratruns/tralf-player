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
username = 'test'
player1 = None
 
class TestPlayer(unittest.TestCase):
    def setUp(self):
        try:
            dbplayer = Player.objects.all()[0]
            self.player1 = dbplayer
        except:
            self.player1 = Player(username=username,question=question,  pub_date=pub_date,  file_name=file_name, frame_num_start=frame_num_start, frame_num_stop=frame_num_stop)

 
    def test___unicode__(self):
        self.assertEqual(str(self.player1),self.player1.question)
        # self.assertEqual(expected, player.__unicode__())

    def test_was_published_today(self):
        pass# player = Player()
        # self.assertEqual(expected, player.was_published_today())
#        assert False # TODO: implement your test here

    def test_Attrib(self):
        self.assertEqual(self.player1.username, username)
        self.assertEqual(self.player1.question, question)
        self.assertEqual(self.player1.pub_date, pub_date)
        self.assertEqual(self.player1.file_name, file_name)
        self.assertEqual(self.player1.frame_num_start, frame_num_start)
        self.assertEqual(self.player1.frame_num_stop, frame_num_stop)




class TestChoice(unittest.TestCase):
    def test___unicode__(self):
        # choice = Choice()
        # self.assertEqual(expected, choice.__unicode__())
        assert False # TODO: implement your test here

class TestFrame(unittest.TestCase):
    def test___unicode__(self):
        # frame = Frame()
        # self.assertEqual(expected, frame.__unicode__())
        assert False # TODO: implement your test here

class TestMedia(unittest.TestCase):
    def test_post_upload_callback(self):
        # media = Media()
        # self.assertEqual(expected, media.post_upload_callback(**kwargs))
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
