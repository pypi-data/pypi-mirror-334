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

class TestScanEvens(unittest.TestCase):
    def setUp(self):
        pass

    def test_not_evens(self):
        self.lexical_analyzer = LexicalAnalyzer("x")
        self.lexical_analyzer.input = InputBuffer("x")
        token = self.lexical_analyzer.scan_evens(tmp=Token(), c='x')
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_rearranged_evens(self):
        self.lexical_analyzer = LexicalAnalyzer("enve")
        self.lexical_analyzer.input = InputBuffer("enve")
        token = self.lexical_analyzer.scan_evens(tmp=Token(), c='s')
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_correct_evens(self):
        self.lexical_analyzer = LexicalAnalyzer("vens")
        self.lexical_analyzer.input = InputBuffer("vens")
        token = self.lexical_analyzer.scan_evens(tmp=Token(), c='e')
        self.assertEqual(token.TokenType, TokenType.BET)
        self.assertEqual(token.lexeme, 'evens')