import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
from operator_precedence_high_roller.parsing.enums.command_type import CommandType
import unittest

class TestParseInit(unittest.TestCase):
    def setUp(self):
        pass

    def test_bet_init(self):
        self.command_parser = CommandParser('odds')
        self.command_parser.parse_init()
        token = self.command_parser.lexer.get_token()
        self.assertEqual(self.command_parser.command_type, CommandType.GAMBLE_BET)
        self.assertEqual(token.TokenType, TokenType.END_OF_FILE)
    
    def test_gamble_init(self):
        self.command_parser = CommandParser('!gamble')
        self.command_parser.parse_init()
        token = self.command_parser.lexer.get_token()
        self.assertEqual(self.command_parser.command_type, CommandType.GAMBLE_START)
        self.assertEqual(token.TokenType, TokenType.END_OF_FILE)

    def test_recall_init(self):
        self.command_parser = CommandParser('!h')
        self.command_parser.parse_init()
        token = self.command_parser.lexer.get_token()
        self.assertEqual(self.command_parser.command_type, CommandType.RECALL_ROLLS)
        self.assertEqual(token.TokenType, TokenType.END_OF_FILE)

    def test_expr_init(self):
        self.command_parser = CommandParser('!5')
        self.command_parser.parse_init()
        token = self.command_parser.lexer.get_token()
        self.assertEqual(self.command_parser.command_type, CommandType.EXPR)
        self.assertEqual(token.TokenType, TokenType.END_OF_FILE)

    def test_error_init(self):
        self.command_parser = CommandParser('error')
        self.command_parser.parse_init()
        self.assertEqual(self.command_parser.command_type, CommandType.ERROR)