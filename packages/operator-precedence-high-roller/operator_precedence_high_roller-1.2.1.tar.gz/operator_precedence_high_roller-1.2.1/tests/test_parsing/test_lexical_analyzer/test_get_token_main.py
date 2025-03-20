import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.lexical_analyzer import LexicalAnalyzer
from operator_precedence_high_roller.parsing.input_buffer import InputBuffer
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
import unittest

class TestGetTokenMain(unittest.TestCase):
    def setUp(self):
        pass

    def test_command_start(self):
        self.lexical_analyzer = LexicalAnalyzer("!")
        self.lexical_analyzer.input = InputBuffer("!")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.COMMAND_START)

    def test_plus(self):
        self.lexical_analyzer = LexicalAnalyzer("+")
        self.lexical_analyzer.input = InputBuffer("+")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.PLUS)

    def test_minus(self):
        self.lexical_analyzer = LexicalAnalyzer("-")
        self.lexical_analyzer.input = InputBuffer("-")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.MINUS)

    def test_mult(self):
        self.lexical_analyzer = LexicalAnalyzer("*")
        self.lexical_analyzer.input = InputBuffer("*")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.MULT)

    def test_div(self):
        self.lexical_analyzer = LexicalAnalyzer("/")
        self.lexical_analyzer.input = InputBuffer("/")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.DIV)

    def test_lparen(self):
        self.lexical_analyzer = LexicalAnalyzer("(")
        self.lexical_analyzer.input = InputBuffer("(")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.LPAREN)

    def test_rparen(self):
        self.lexical_analyzer = LexicalAnalyzer(")")
        self.lexical_analyzer.input = InputBuffer(")")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.RPAREN)

    def test_comma(self):
        self.lexical_analyzer = LexicalAnalyzer(",")
        self.lexical_analyzer.input = InputBuffer(",")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.COMMA)

    def test_num(self):
        self.lexical_analyzer = LexicalAnalyzer("6")
        self.lexical_analyzer.input = InputBuffer("6")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.NUM)
        self.assertEqual(token.lexeme, "6")

    def test_roll_multiple_dice(self):
        self.lexical_analyzer = LexicalAnalyzer("6d6")
        self.lexical_analyzer.input = InputBuffer("6d6")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, "6d6")

    def test_roll_die(self):
        self.lexical_analyzer = LexicalAnalyzer("d6")
        self.lexical_analyzer.input = InputBuffer("d6")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, "d6")

    def test_roll_exploding_die(self):
        self.lexical_analyzer = LexicalAnalyzer("e6")
        self.lexical_analyzer.input = InputBuffer("e6")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, "e6")

    def test_odds(self):
        self.lexical_analyzer = LexicalAnalyzer("odds")
        self.lexical_analyzer.input = InputBuffer("odds")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.BET)

    def test_evens(self):
        self.lexical_analyzer = LexicalAnalyzer("evens")
        self.lexical_analyzer.input = InputBuffer("evens")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.BET)

    def test_recall(self):
        self.lexical_analyzer = LexicalAnalyzer("h")
        self.lexical_analyzer.input = InputBuffer("h")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.RECALL)

    def test_error(self):
        self.lexical_analyzer = LexicalAnalyzer("x")
        self.lexical_analyzer.input = InputBuffer("x")
        token = self.lexical_analyzer.get_token_main()
        self.assertEqual(token.TokenType, TokenType.ERROR)