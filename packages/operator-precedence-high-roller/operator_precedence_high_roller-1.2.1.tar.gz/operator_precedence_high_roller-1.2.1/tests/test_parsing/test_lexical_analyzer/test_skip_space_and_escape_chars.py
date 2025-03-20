import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[3]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.lexical_analyzer import LexicalAnalyzer
import unittest

class TestSkipSpaceAndEscapeChars(unittest.TestCase):
    def setUp(self):
        pass

    def test_no_white_space(self):
        self.lexical_analyzer = LexicalAnalyzer("!d20+5")
        self.lexical_analyzer.skip_space_and_escape_chars()
        c = self.lexical_analyzer.input.get_char()
        self.assertFalse(self.lexical_analyzer.isspace(c))
        self.lexical_analyzer.input.unget_char(c)

    def test_one_white_space(self):
        self.lexical_analyzer = LexicalAnalyzer("!d20 +5")
        self.lexical_analyzer.skip_space_and_escape_chars()
        c = self.lexical_analyzer.input.get_char()
        self.assertFalse(self.lexical_analyzer.isspace(c))
        self.lexical_analyzer.input.unget_char(c)

    def test_separate_white_space(self):
        self.lexical_analyzer = LexicalAnalyzer("!d20 + 5")
        self.lexical_analyzer.skip_space_and_escape_chars()
        c = self.lexical_analyzer.input.get_char()
        self.assertFalse(self.lexical_analyzer.isspace(c))
        self.lexical_analyzer.input.unget_char(c)

    def test_one_escape_char(self):
        self.lexical_analyzer = LexicalAnalyzer("!\d20 +5")
        self.lexical_analyzer.skip_space_and_escape_chars()
        c = self.lexical_analyzer.input.get_char()
        self.assertFalse(c == '\\')
        self.lexical_analyzer.input.unget_char(c)

    def test_two_escape_chars(self):
        self.lexical_analyzer = LexicalAnalyzer("!d20+(2\*d4+3\*d6)")
        self.lexical_analyzer.skip_space_and_escape_chars()
        c = self.lexical_analyzer.input.get_char()
        self.assertFalse(c == '\\')
        self.lexical_analyzer.input.unget_char(c)