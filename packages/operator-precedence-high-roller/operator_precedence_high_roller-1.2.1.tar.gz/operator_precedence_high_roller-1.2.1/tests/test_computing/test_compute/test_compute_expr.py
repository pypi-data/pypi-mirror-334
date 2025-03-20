import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.computing.compute import Compute
from operator_precedence_high_roller.parsing.stacknode import StackNode
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
import unittest

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.compute = Compute()

    def test_oper_plus(self):
        left = StackNode()
        left.token_info.lexeme = "1"
        left.token_info.TokenType = TokenType.NUM
        right = StackNode()
        right.token_info.lexeme = "1"
        right.token_info.TokenType = TokenType.NUM
        oper_plus = StackNode()
        oper_plus.left = left
        oper_plus.right = right
        oper_plus.oper = TokenType.PLUS
        self.assertEqual(self.compute.compute_expr(oper_plus), (2,2))

    def test_oper_minus(self):
        left = StackNode()
        left.token_info.lexeme = "1"
        left.token_info.TokenType = TokenType.NUM
        right = StackNode()
        right.token_info.lexeme = "1"
        right.token_info.TokenType = TokenType.NUM
        oper_minus = StackNode()
        oper_minus.left = left
        oper_minus.right = right
        oper_minus.oper = TokenType.MINUS
        self.assertEqual(self.compute.compute_expr(oper_minus), (0,0))

    def test_oper_mult(self):
        left = StackNode()
        left.token_info.lexeme = "1"
        left.token_info.TokenType = TokenType.NUM
        right = StackNode()
        right.token_info.lexeme = "1"
        right.token_info.TokenType = TokenType.NUM
        oper_mult = StackNode()
        oper_mult.left = left
        oper_mult.right = right
        oper_mult.oper = TokenType.MULT
        self.assertEqual(self.compute.compute_expr(oper_mult), (1,1))

    def test_oper_div(self):
        left = StackNode()
        left.token_info.lexeme = "1"
        left.token_info.TokenType = TokenType.NUM
        right = StackNode()
        right.token_info.lexeme = "1"
        right.token_info.TokenType = TokenType.NUM
        oper_div = StackNode()
        oper_div.left = left
        oper_div.right = right
        oper_div.oper = TokenType.DIV
        self.assertEqual(self.compute.compute_expr(oper_div), (1,1))

    def test_oper_div_by_0(self):
        left = StackNode()
        left.token_info.lexeme = "1"
        left.token_info.TokenType = TokenType.NUM
        right = StackNode()
        right.token_info.lexeme = "0"
        right.token_info.TokenType = TokenType.NUM
        oper_div = StackNode()
        oper_div.left = left
        oper_div.right = right
        oper_div.oper = TokenType.DIV
        self.assertEqual(self.compute.compute_expr(oper_div), 0)
        self.assertTrue(self.compute.error)

    def test_error(self):
        error = StackNode()
        error.token_info.TokenType = TokenType.ERROR
        self.compute.compute_expr(error)
        self.assertTrue(self.compute.error)

    def test_roll(self):
        roll = StackNode()
        roll.token_info.lexeme = "d2"
        roll.token_info.TokenType = TokenType.ROLL
        self.assertIn(
            self.compute.compute_expr(roll), [
                (1,1),
                (2,1)
            ])
        
    def test_exploding_roll(self):
        roll = StackNode()
        roll.token_info.lexeme = "e1"
        roll.token_info.TokenType = TokenType.ROLL
        self.assertEqual(self.compute.compute_expr(roll), (1,1))

    def test_num(self):
        num = StackNode()
        num.token_info.lexeme = "1"
        num.token_info.TokenType = TokenType.NUM
        self.assertEqual(self.compute.compute_expr(num), (1,1))