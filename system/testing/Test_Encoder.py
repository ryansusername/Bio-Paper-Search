import unittest
from encoder import extract_sentences, encoder_bert

example_text: 'This is Sentence One. This is Sentence Two. This is Sentence Three'
sentences = ['This is Sentence One', 'This is Sentence Two', 'This is Sentence Three']


class Test_EncoderModule(unittest.TestCase):
    def TestSentenceTokenise(self):
        sent = sentences_from_text(example_paragrah)
        self.assertEqual(sent, sentences)
