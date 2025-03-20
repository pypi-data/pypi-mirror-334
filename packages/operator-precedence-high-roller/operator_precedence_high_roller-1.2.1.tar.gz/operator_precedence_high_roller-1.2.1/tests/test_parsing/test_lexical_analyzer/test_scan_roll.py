import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.lexical_analyzer import LexicalAnalyzer
from operator_precedence_high_roller.parsing.input_buffer import InputBuffer
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
import unittest

class TestScanRoll(unittest.TestCase):
    def setUp(self):
        pass

    def test_not_single_roll(self):
        self.lexical_analyzer = LexicalAnalyzer("2d6")
        self.lexical_analyzer.input = InputBuffer("2d6")
        token = self.lexical_analyzer.scan_roll()
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_not_roll(self):
        self.lexical_analyzer = LexicalAnalyzer("2dnot a roll")
        self.lexical_analyzer.input = InputBuffer("2dnot a roll")
        token = self.lexical_analyzer.scan_roll()
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_roll(self):
        self.lexical_analyzer = LexicalAnalyzer("d20")
        self.lexical_analyzer.input = InputBuffer("d20")
        token = self.lexical_analyzer.scan_roll()
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, 'd20')