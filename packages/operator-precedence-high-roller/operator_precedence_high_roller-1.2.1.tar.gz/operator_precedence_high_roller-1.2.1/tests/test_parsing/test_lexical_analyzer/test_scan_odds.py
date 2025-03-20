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

class TestScanOdds(unittest.TestCase):
    def setUp(self):
        pass

    def test_not_odds(self):
        self.lexical_analyzer = LexicalAnalyzer("x")
        self.lexical_analyzer.input = InputBuffer("x")
        token = self.lexical_analyzer.scan_odds(tmp=Token(), c='x')
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_rearranged_odds(self):
        self.lexical_analyzer = LexicalAnalyzer("osd")
        self.lexical_analyzer.input = InputBuffer("osd")
        token = self.lexical_analyzer.scan_odds(tmp=Token(), c='d')
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_correct_odds(self):
        self.lexical_analyzer = LexicalAnalyzer("dds")
        self.lexical_analyzer.input = InputBuffer("dds")
        token = self.lexical_analyzer.scan_odds(tmp=Token(), c='o')
        self.assertEqual(token.TokenType, TokenType.BET)
        self.assertEqual(token.lexeme, 'odds')