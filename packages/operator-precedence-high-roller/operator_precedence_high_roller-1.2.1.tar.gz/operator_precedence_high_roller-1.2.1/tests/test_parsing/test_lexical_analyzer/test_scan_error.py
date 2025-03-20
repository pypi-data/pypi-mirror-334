import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.lexical_analyzer import LexicalAnalyzer
from operator_precedence_high_roller.parsing.input_buffer import InputBuffer
from operator_precedence_high_roller.parsing.command_token import Token
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
import unittest

class TestEndOfInput(unittest.TestCase):
    def setUp(self):
        pass

    def test_not_end_of_input(self):
        self.ib = InputBuffer("")
        self.lexical_analyzer = LexicalAnalyzer("!d20+5")
        self.ib.input_buffer = ['c']
        self.assertEqual(self.lexical_analyzer.scan_error(tmp=Token(), c='c').TokenType, TokenType.ERROR)

    def test_end_of_input(self):
        self.ib = InputBuffer("")
        self.lexical_analyzer = LexicalAnalyzer("!d20+5")
        self.ib.input_buffer = []
        self.assertEqual(self.lexical_analyzer.scan_error(tmp=Token(), c='c').TokenType, TokenType.ERROR)