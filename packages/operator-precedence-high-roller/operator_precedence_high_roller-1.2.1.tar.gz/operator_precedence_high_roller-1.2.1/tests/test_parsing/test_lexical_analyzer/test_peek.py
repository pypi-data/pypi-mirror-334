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

class TestPeek(unittest.TestCase):
    def setUp(self):
        pass

    def test_non_positive(self):
        self.lexical_analyzer = LexicalAnalyzer("")
        self.assertEqual(self.lexical_analyzer.peek(-1), None)

    def test_peek_past_end(self):
        self.lexical_analyzer = LexicalAnalyzer("")
        self.lexical_analyzer.token_list = []
        self.lexical_analyzer.index = 1
        token = self.lexical_analyzer.peek(1)
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