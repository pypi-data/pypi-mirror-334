import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
from operator_precedence_high_roller.parsing.enums.command_type import CommandType
import unittest

class TestExpect(unittest.TestCase):
    def setUp(self):
        pass

    def test_expect_match(self):
        self.command_parser = CommandParser('!')
        token = self.command_parser.expect(TokenType.COMMAND_START)
        self.assertEqual(token.TokenType, TokenType.COMMAND_START)

    def test_expect_mismatch(self):
        self.command_parser = CommandParser('x')
        self.assertEqual(self.command_parser.expect(TokenType.COMMAND_START), None)
        self.assertEqual(self.command_parser.command_type, CommandType.ERROR)