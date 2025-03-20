import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
from operator_precedence_high_roller.parsing.enums.command_type import CommandType
import unittest

class TestParseRecall(unittest.TestCase):
    def setUp(self):
        pass

    def test_recall_init(self):
        self.command_parser = CommandParser('h')
        self.command_parser.parse_recall()
        token = self.command_parser.lexer.get_token()
        self.assertEqual(self.command_parser.command_type, CommandType.RECALL_ROLLS)
        self.assertEqual(token.TokenType, TokenType.END_OF_FILE)

    def test_recall_num_and_roll(self):
        self.command_parser = CommandParser('h(1,d20)')
        self.command_parser.parse_recall()
        token = self.command_parser.lexer.get_token()
        self.assertEqual(self.command_parser.command_type, CommandType.RECALL_ROLLS)
        self.assertEqual(token.TokenType, TokenType.END_OF_FILE)

    def test_recall_roll_only(self):
        self.command_parser = CommandParser('h(d20)')
        self.command_parser.parse_recall()
        token = self.command_parser.lexer.get_token()
        self.assertEqual(self.command_parser.command_type, CommandType.RECALL_ROLLS)
        self.assertEqual(token.TokenType, TokenType.END_OF_FILE)

    def test_recall_bad_syntax(self):
        self.command_parser = CommandParser('h(,)')
        self.command_parser.parse_recall()
        self.assertEqual(self.command_parser.command_type, CommandType.ERROR)