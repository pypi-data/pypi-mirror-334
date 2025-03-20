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

class TestScanBet(unittest.TestCase):
    def setUp(self):
        pass

    def test_not_bet(self):
        self.lexical_analyzer = LexicalAnalyzer("x")
        self.lexical_analyzer.input = InputBuffer("x")
        token = self.lexical_analyzer.scan_bet()
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_just_e(self):
        self.lexical_analyzer = LexicalAnalyzer("eee")
        self.lexical_analyzer.input = InputBuffer("eee")
        token = self.lexical_analyzer.scan_bet()
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_just_o(self):
        self.lexical_analyzer = LexicalAnalyzer("ooo")
        self.lexical_analyzer.input = InputBuffer("ooo")
        token = self.lexical_analyzer.scan_bet()
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_correct_evens(self):
        self.lexical_analyzer = LexicalAnalyzer("evens")
        self.lexical_analyzer.input = InputBuffer("evens")
        token = self.lexical_analyzer.scan_bet()
        self.assertEqual(token.TokenType, TokenType.BET)

    def test_correct_odds(self):
        self.lexical_analyzer = LexicalAnalyzer("odds")
        self.lexical_analyzer.input = InputBuffer("odds")
        token = self.lexical_analyzer.scan_bet()
        self.assertEqual(token.TokenType, TokenType.BET)