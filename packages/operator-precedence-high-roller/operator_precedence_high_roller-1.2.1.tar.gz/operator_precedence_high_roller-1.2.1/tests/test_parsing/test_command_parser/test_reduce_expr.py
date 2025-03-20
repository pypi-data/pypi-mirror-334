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

class TestReduceExpr(unittest.TestCase):
    def setUp(self):
        pass

    def test_roll(self):
        self.command_parser = CommandParser("")
        node = StackNode()
        node.token_info.TokenType = TokenType.ROLL
        self.command_parser.rhs = [node]
        test_node = self.command_parser.reduce_expr()
        new_node = StackNode()
        new_node.is_terminal = False
        new_node.token_info = self.command_parser.rhs[0].token_info
        self.assertEqual(test_node.is_terminal, new_node.is_terminal)
        self.assertEqual(test_node.token_info.TokenType, new_node.token_info.TokenType)

    def test_num(self):
        self.command_parser = CommandParser("")
        node = StackNode()
        node.token_info.TokenType = TokenType.NUM
        self.command_parser.rhs = [node]
        test_node = self.command_parser.reduce_expr()
        new_node = StackNode()
        new_node.is_terminal = False
        new_node.token_info = self.command_parser.rhs[0].token_info
        self.assertEqual(test_node.is_terminal, new_node.is_terminal)
        self.assertEqual(test_node.token_info.TokenType, new_node.token_info.TokenType)

    def test_arithm_expr(self):
        self.command_parser = CommandParser("")
        node1 = StackNode()
        node1.is_terminal = False
        node2 = StackNode()
        node2.token_info.TokenType = TokenType.PLUS
        node3 = StackNode()
        node3.is_terminal = False
        self.command_parser.rhs = [node1, node2, node3]

        test_node = self.command_parser.reduce_expr()

        new_node = StackNode()
        new_node.is_terminal = False
        new_node.token_info = Token()
        new_node.oper = TokenType.PLUS
        new_node.left = node3
        new_node.right = node1

        self.assertEqual(test_node.left.is_terminal, new_node.left.is_terminal)
        self.assertEqual(test_node.right.is_terminal, new_node.right.is_terminal)
        self.assertEqual(test_node.oper, new_node.oper)

    def test_arithm_expr(self):
        self.command_parser = CommandParser("")
        node1 = StackNode()
        node1.token_info.TokenType = TokenType.RPAREN
        node2 = StackNode()
        node2.is_terminal = False
        node3 = StackNode()
        node3.token_info.TokenType = TokenType.LPAREN
        self.command_parser.rhs = [node1, node2, node3]

        test_node = self.command_parser.reduce_expr()

        new_node = StackNode()
        new_node.is_terminal = False
        new_node = node2

        self.assertEqual(test_node.is_terminal, new_node.is_terminal)

