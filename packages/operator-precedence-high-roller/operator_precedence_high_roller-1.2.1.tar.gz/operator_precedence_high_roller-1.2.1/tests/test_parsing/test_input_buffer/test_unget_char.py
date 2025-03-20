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

    def test_c_too_long(self):
        self.ib = InputBuffer("")
        with self.assertRaises(TypeError):
            self.ib.unget_char('cc')

    def test_c_not_eof(self):
        self.ib = InputBuffer("")
        self.ib.input_buffer = []
        self.ib.unget_char('c')
        self.assertEqual(self.ib.input_buffer, ['c'])