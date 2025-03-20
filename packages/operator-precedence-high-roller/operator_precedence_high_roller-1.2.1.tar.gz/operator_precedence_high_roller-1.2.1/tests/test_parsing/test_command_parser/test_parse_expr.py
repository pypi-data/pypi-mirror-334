import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
from operator_precedence_high_roller.parsing.enums.command_type import CommandType
from operator_precedence_high_roller.parsing.command_token import Token
from operator_precedence_high_roller.parsing.stacknode import StackNode
import unittest

class TestParseExpr(unittest.TestCase):
    def setUp(self):
        pass

    def test_num_expr(self):
        self.command_parser = CommandParser("!5")
        self.command_parser.parse_init()
        self.assertTrue(len(self.command_parser.stack) == 2)
        self.assertTrue(self.command_parser.stack[0].is_terminal)
        self.assertFalse(self.command_parser.stack[1].is_terminal)

    def test_roll_expr(self):
        self.command_parser = CommandParser("!d20")
        self.command_parser.parse_init()
        self.assertTrue(len(self.command_parser.stack) == 2)
        self.assertTrue(self.command_parser.stack[0].is_terminal)
        self.assertFalse(self.command_parser.stack[1].is_terminal)

    def test_arithm_expr(self):
        self.command_parser = CommandParser("!d20+5")
        self.command_parser.parse_init()
        self.assertTrue(len(self.command_parser.stack) == 2)
        self.assertTrue(self.command_parser.stack[0].is_terminal)
        self.assertFalse(self.command_parser.stack[1].is_terminal)

    def test_closed_par_expr(self):
        self.command_parser = CommandParser("!(d20)")
        self.command_parser.parse_init()
        self.assertTrue(len(self.command_parser.stack) == 2)
        self.assertTrue(self.command_parser.stack[0].is_terminal)
        self.assertFalse(self.command_parser.stack[1].is_terminal)