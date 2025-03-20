import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
from operator_precedence_high_roller.parsing.command_token import Token
from operator_precedence_high_roller.parsing.enums.command_type import CommandType
from operator_precedence_high_roller.parsing.stacknode import StackNode
import unittest

class TestParseRecall(unittest.TestCase):
    def setUp(self):
        pass

    def test_top_of_stack(self):
        self.command_parser = CommandParser("")
        node = StackNode()
        node.is_terminal = True
        self.command_parser.stack = [node]
        self.assertEqual(self.command_parser.terminal_peek(), self.command_parser.stack[-1])

    def test_second_from_top_of_stack(self):
        self.command_parser = CommandParser("")
        node1 = StackNode()
        node1.is_terminal = True
        node2 = StackNode()
        node2.is_terminal = False
        self.command_parser.stack = [node1, node2]
        self.assertEqual(self.command_parser.terminal_peek(), self.command_parser.stack[-2])

    def test_top_two_nonterminal(self):
        self.command_parser = CommandParser("")
        node1 = StackNode()
        node1.is_terminal = True
        node2 = StackNode()
        node2.is_terminal = False
        node3 = StackNode()
        node3.is_terminal = False
        self.command_parser.stack = [node1, node2, node3]
        self.assertEqual(self.command_parser.terminal_peek(), None)