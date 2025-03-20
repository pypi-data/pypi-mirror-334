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

class TestScanNumberOrRoll(unittest.TestCase):
    def setUp(self):
        pass

    def test_not_digit(self):
        self.lexical_analyzer = LexicalAnalyzer("c")
        self.lexical_analyzer.input = InputBuffer("c")
        token = self.lexical_analyzer.scan_number_or_roll()
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_one_digit_number(self):
        self.lexical_analyzer = LexicalAnalyzer("1")
        self.lexical_analyzer.input = InputBuffer("1")
        token = self.lexical_analyzer.scan_number_or_roll()
        self.assertEqual(token.TokenType, TokenType.NUM)
        self.assertEqual(token.lexeme, '1')

    def test_two_digit_number(self):
        self.lexical_analyzer = LexicalAnalyzer("12")
        self.lexical_analyzer.input = InputBuffer("12")
        token = self.lexical_analyzer.scan_number_or_roll()
        self.assertEqual(token.TokenType, TokenType.NUM)
        self.assertEqual(token.lexeme, '12')

    def test_one_digit_num_rolls(self):
        self.lexical_analyzer = LexicalAnalyzer("2d6")
        self.lexical_analyzer.input = InputBuffer("2d6")
        token = self.lexical_analyzer.scan_number_or_roll()
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, '2d6')

    def test_two_digit_num_rolls(self):
        self.lexical_analyzer = LexicalAnalyzer("12d6")
        self.lexical_analyzer.input = InputBuffer("12d6")
        token = self.lexical_analyzer.scan_number_or_roll()
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, '12d6')

    def test_one_digit_num_rolls_keep_highest_one(self):
        self.lexical_analyzer = LexicalAnalyzer("2d6kh")
        self.lexical_analyzer.input = InputBuffer("2d6kh")
        token = self.lexical_analyzer.scan_number_or_roll()
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, '2d6kh')

    def test_one_digit_num_rolls_keep_highest_2(self):
        self.lexical_analyzer = LexicalAnalyzer("3d6kh2")
        self.lexical_analyzer.input = InputBuffer("3d6kh2")
        token = self.lexical_analyzer.scan_number_or_roll()
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, '3d6kh2')