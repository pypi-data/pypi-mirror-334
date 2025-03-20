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
        self.assertFalse(self.ib.end_of_input())

    def test_input_buffer_empty_eof_true(self):
        self.ib = InputBuffer("")
        self.ib.input_buffer = []
        self.ib.eof = True
        self.assertTrue(self.ib.end_of_input())

    def test_input_buffer_empty_eof_false(self):
        self.ib = InputBuffer("")
        self.ib.input_buffer = []
        self.ib.eof = False
        self.assertFalse(self.ib.end_of_input())