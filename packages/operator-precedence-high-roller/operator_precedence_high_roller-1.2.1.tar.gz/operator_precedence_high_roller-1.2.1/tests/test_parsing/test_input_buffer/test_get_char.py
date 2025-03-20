import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.input_buffer import InputBuffer
import unittest

class TestEndOfInput(unittest.TestCase):
    def setUp(self):
        pass

    def test_input_buffer_not_empty(self):
        self.ib = InputBuffer("")
        self.ib.input_buffer = ['c']
        self.assertEqual(self.ib.get_char(), 'c')

    def test_input_string_not_empty(self):
        self.ib = InputBuffer("c")
        self.assertEqual(self.ib.get_char(), 'c')

    def test_input_string_and_input_buffer_empty(self):
        self.ib = InputBuffer("")
        self.assertEqual(self.ib.get_char(), '$')