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

class TestIsValidExpr(unittest.TestCase):
    def setUp(self):
        self.command_parser = CommandParser("")
        self.node1 = StackNode()
        self.node1.is_terminal = True
        self.node1.token_info.TokenType = TokenType.END_OF_FILE
        self.node1.token_info.lexeme = ''

    def test_roll_expr(self):
        self.node2 = StackNode()
        self.node1.is_terminal = True
        self.node2.token_info.TokenType = TokenType.ROLL
        self.node2.token_info.lexeme = 'd20'
        self.command_parser.stack = [self.node1, self.node2]
        self.command_parser.reduce()
        self.assertTrue(len(self.command_parser.stack) == 2)
        self.assertTrue(self.command_parser.stack[0].is_terminal)
        self.assertFalse(self.command_parser.stack[1].is_terminal)

    def test_num_expr(self):
        self.node2 = StackNode()
        self.node1.is_terminal = True
        self.node2.token_info.TokenType = TokenType.NUM
        self.node2.token_info.lexeme = '5'
        self.command_parser.stack = [self.node1, self.node2]
        self.command_parser.reduce()
        self.assertTrue(len(self.command_parser.stack) == 2)
        self.assertTrue(self.command_parser.stack[0].is_terminal)
        self.assertFalse(self.command_parser.stack[1].is_terminal)

    def test_arithm_expr(self):
        self.command_parser = CommandParser("")
        self.node2 = StackNode()
        self.node2.is_terminal = False
        self.node3 = StackNode()
        self.node3.token_info.TokenType = TokenType.PLUS
        self.node4 = StackNode()
        self.node4.is_terminal = False
        self.command_parser.stack = [self.node1, self.node2, self.node3, self.node4]
        self.command_parser.reduce()
        self.assertTrue(len(self.command_parser.stack) == 2)
        self.assertTrue(self.command_parser.stack[0].is_terminal)
        self.assertFalse(self.command_parser.stack[1].is_terminal)

    def test_closed_par_expr(self):
        self.command_parser = CommandParser("")
        self.node2 = StackNode()
        self.node2.is_terminal = False
        self.node3 = StackNode()
        self.node3.is_terminal = False
        self.node4 = StackNode()
        self.node4.is_terminal = False
        self.command_parser.stack = [self.node1, self.node2, self.node3, self.node4]
        self.assertEqual(self.command_parser.reduce(), None)
        self.assertEqual(self.command_parser.command_type, CommandType.ERROR)
        