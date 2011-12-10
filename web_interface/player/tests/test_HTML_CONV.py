import settings
import unittest
import player.HTML_CONV
from player.models import Player, Choice, Frame


class TestPlaintext2html(unittest.TestCase):
    def test_plaintext2html(self):
        frames = Frame.objects.all()
        count = 0
        for f in frames:
            count += 1
            new_frame_text = HTML_CONV.plaintext2html(text=f.frame)
            self.assertEqual(f.frame, new_frame_text) 
            if count >= 5: #only test first five to save time
                break

if __name__ == '__main__':
    unittest.main()
