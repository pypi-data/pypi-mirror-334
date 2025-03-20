import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller import message_validator
from tests.mock_classes.mock_message_attributes.mock_author import MockAuthor
from tests.mock_classes.mock_message import MockMessage
import unittest

class TestMessageIsCommand(unittest.TestCase):
    def setUp(self):
        self.author = MockAuthor(name = 'test_1234')

    def test_length_0_message(self):
        self.message = MockMessage(self.author, None, '')
        self.assertEqual(message_validator.message_is_command(self.message), False)

    def test_excl_at_index_0(self):
        self.message = MockMessage(self.author, None, '!')
        self.assertEqual(message_validator.message_is_command(self.message), True)

    def test_odds(self):
        self.message = MockMessage(self.author, None, 'odds')
        self.assertEqual(message_validator.message_is_command(self.message), True)

    def test_evens(self):
        self.message = MockMessage(self.author, None, 'evens')
        self.assertEqual(message_validator.message_is_command(self.message), True)

    def test_noncommand(self):
        self.message = MockMessage(self.author, None, 'this is not a command')
        self.assertEqual(message_validator.message_is_command(self.message), False)