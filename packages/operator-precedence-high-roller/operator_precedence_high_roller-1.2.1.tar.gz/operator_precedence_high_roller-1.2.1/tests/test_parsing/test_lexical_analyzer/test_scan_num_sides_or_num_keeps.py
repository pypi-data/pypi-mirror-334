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

class TestScanNumSidesOrNumKeeps(unittest.TestCase):
    def setUp(self):
        pass

    def test_one_digit(self):
        self.lexical_analyzer = LexicalAnalyzer("")
        self.lexical_analyzer.input = InputBuffer("")
        token = self.lexical_analyzer.scan_num_sides_or_num_keeps(tmp=Token(), c='1')
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, '1')

    def test_two_digits(self):
        self.lexical_analyzer = LexicalAnalyzer("2")
        self.lexical_analyzer.input = InputBuffer("2")
        token = self.lexical_analyzer.scan_num_sides_or_num_keeps(tmp=Token(), c='1')
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, '12')

    def test_with_dice(self):
        self.lexical_analyzer = LexicalAnalyzer("d6")
        self.lexical_analyzer.input = InputBuffer("d6")
        token = self.lexical_analyzer.scan_num_sides_or_num_keeps(tmp=Token(), c='3')
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, '3')

    def test_with_ten_dice(self):
        self.lexical_analyzer = LexicalAnalyzer("0d6")
        self.lexical_analyzer.input = InputBuffer("0d6")
        token = self.lexical_analyzer.scan_num_sides_or_num_keeps(tmp=Token(), c='1')
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, '10')