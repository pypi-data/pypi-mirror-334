import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
from operator_precedence_high_roller.parsing.command_token import Token
from operator_precedence_high_roller.parsing.stacknode import StackNode
import unittest

class TestDetermineOperation(unittest.TestCase):
    def setUp(self):
        pass

    def test_plus(self):
        self.command_parser = CommandParser("")
        node = StackNode()
        node.token_info.TokenType = TokenType.PLUS
        self.command_parser.rhs = [None, node, None]
        self.assertEqual(self.command_parser.determine_operation(), TokenType.PLUS)

    def test_minus(self):
        self.command_parser = CommandParser("")
        node = StackNode()
        node.token_info.TokenType = TokenType.MINUS
        self.command_parser.rhs = [None, node, None]
        self.assertEqual(self.command_parser.determine_operation(), TokenType.MINUS)

    def test_mult(self):
        self.command_parser = CommandParser("")
        node = StackNode()
        node.token_info.TokenType = TokenType.MULT
        self.command_parser.rhs = [None, node, None]
        self.assertEqual(self.command_parser.determine_operation(), TokenType.MULT)

    def test_div(self):
        self.command_parser = CommandParser("")
        node = StackNode()
        node.token_info.TokenType = TokenType.DIV
        self.command_parser.rhs = [None, node, None]
        self.assertEqual(self.command_parser.determine_operation(), TokenType.DIV)

    def test_error(self):
        self.command_parser = CommandParser("")
        node = StackNode()
        node.token_info.TokenType = TokenType.COMMAND_START
        self.command_parser.rhs = [None, node, None]
        self.assertEqual(self.command_parser.determine_operation(), TokenType.ERROR)

    