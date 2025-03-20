import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.lexical_analyzer import LexicalAnalyzer
from operator_precedence_high_roller.parsing.input_buffer import InputBuffer
from operator_precedence_high_roller.parsing.command_token import Token
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
import unittest

class TestScanRecall(unittest.TestCase):
    def setUp(self):
        pass

    def test_not_recall(self):
        self.lexical_analyzer = LexicalAnalyzer("x")
        self.lexical_analyzer.input = InputBuffer("x")
        token = self.lexical_analyzer.scan_recall()
        self.assertEqual(token.TokenType, TokenType.ERROR)

    def test_recall(self):
        self.lexical_analyzer = LexicalAnalyzer("h")
        self.lexical_analyzer.input = InputBuffer("h")
        token = self.lexical_analyzer.scan_recall()
        self.assertEqual(token.TokenType, TokenType.RECALL)