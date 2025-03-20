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

class TestGetToken(unittest.TestCase):
    def setUp(self):
        pass

    def test_at_eof(self):
        self.lexical_analyzer = LexicalAnalyzer("x")
        self.lexical_analyzer.input = InputBuffer("x")
        self.lexical_analyzer.index = 1
        token = self.lexical_analyzer.get_token()
        self.assertEqual(token.TokenType, TokenType.END_OF_FILE)
        self.assertEqual(token.lexeme, "")

    def test_at_start(self):
        self.lexical_analyzer = LexicalAnalyzer("")
        token_in = Token()
        token_in.lexeme = "!"
        token_in.TokenType = TokenType.COMMAND_START
        self.lexical_analyzer.token_list = [token_in]
        self.lexical_analyzer.index = 0
        token = self.lexical_analyzer.get_token()
        self.assertEqual(token.TokenType, TokenType.COMMAND_START)
        self.assertEqual(token.lexeme, "!")

    def test_peek_within(self):
        self.lexical_analyzer = LexicalAnalyzer("")
        token1 = Token()
        token1.lexeme = "!"
        token1.TokenType = TokenType.COMMAND_START
        token2 = Token()
        token2.lexeme = "d20"
        token2.TokenType = TokenType.ROLL
        self.lexical_analyzer.token_list = [token1, token2]
        self.lexical_analyzer.index = 1
        token = self.lexical_analyzer.get_token()
        self.assertEqual(token.TokenType, TokenType.ROLL)
        self.assertEqual(token.lexeme, "d20")