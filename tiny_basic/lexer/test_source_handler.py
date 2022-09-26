import unittest

from .source_handler import source_from_string


class SourceHandlerTest(unittest.TestCase):
    def test_empty(self):
        src_handler = source_from_string('')
        self.assertTrue(src_handler.eof())
        self.assertEqual('', src_handler.get_char())

    def test_one(self):
        src_handler = source_from_string('a')
        self.assertFalse(src_handler.eof())
        self.assertEqual('a', src_handler.get_char())
        self.assertFalse(src_handler.eof())
        self.assertEqual('', src_handler.get_char())
        self.assertTrue(src_handler.eof())

    def test_sequence(self):
        src_handler = source_from_string('abc')
        self.assertFalse(src_handler.eof())
        self.assertEqual('a', src_handler.get_char())
        self.assertFalse(src_handler.eof())
        self.assertEqual('b', src_handler.get_char())
        self.assertFalse(src_handler.eof())
        self.assertEqual('c', src_handler.get_char())
        self.assertFalse(src_handler.eof())
        self.assertEqual('', src_handler.get_char())
        self.assertTrue(src_handler.eof())
