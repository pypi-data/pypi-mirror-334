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

class TestIsValidExpr(unittest.TestCase):
    def setUp(self):
        pass

    def test_roll_expr(self):
        self.command_parser = CommandParser("")
        node = StackNode()
        node.is_terminal = True
        node.token_info = Token()
        node.token_info.TokenType = TokenType.ROLL
        node.token_info.lexeme = 'd20'
        self.command_parser.rhs = [node]
        self.assertTrue(self.command_parser.is_valid_expr())

    def test_num_expr(self):
        self.command_parser = CommandParser("")
        node = StackNode()
        node.is_terminal = True
        node.token_info = Token()
        node.token_info.TokenType = TokenType.NUM
        node.token_info.lexeme = '5'
        self.command_parser.rhs = [node]
        self.assertTrue(self.command_parser.is_valid_expr())

    def test_arithm_expr(self):
        self.command_parser = CommandParser("")
        node1 = StackNode()
        node1.is_terminal = False
        node2 = StackNode()
        node2.token_info.TokenType = TokenType.PLUS
        node3 = StackNode()
        node3.is_terminal = False
        self.command_parser.rhs = [node1, node2, node3]
        self.assertTrue(self.command_parser.is_valid_expr())
        
    def test_closed_par_expr(self):
        self.command_parser = CommandParser("")
        node1 = StackNode()
        node1.token_info.TokenType = TokenType.RPAREN
        node2 = StackNode()
        node2.is_terminal = False
        node2.token_info.TokenType = TokenType.NUM
        node3 = StackNode()
        node3.token_info.TokenType = TokenType.LPAREN
        self.command_parser.rhs = [node1, node2, node3]
        self.assertTrue(self.command_parser.is_valid_expr())

    def test_paren_error(self):
        self.command_parser = CommandParser("")
        node1 = StackNode()
        node1.token_info.TokenType = TokenType.RPAREN
        self.command_parser.rhs = [node1]
        self.assertFalse(self.command_parser.is_valid_expr())