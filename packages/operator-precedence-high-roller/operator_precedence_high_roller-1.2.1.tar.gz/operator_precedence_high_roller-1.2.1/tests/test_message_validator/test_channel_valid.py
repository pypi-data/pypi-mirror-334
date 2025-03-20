import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller import message_validator
from tests.mock_classes.mock_message_attributes.mock_author import MockAuthor
from tests.mock_classes.mock_message_attributes.mock_channel import MockChannel
from tests.mock_classes.mock_message import MockMessage
import unittest

class TestChannelValid(unittest.TestCase):
    def setUp(self):
        self.author = MockAuthor(name = 'test_1234')

    def test_dnd_in_channel(self):
        self.channel = MockChannel(name = 'dnd_channel')
        self.message = MockMessage(self.author, self.channel, None)
        self.assertEqual(message_validator.channel_valid(self.message), True)

    def test_invalid_channel(self):
        self.channel = MockChannel(name = 'this-is-not-a-valid-channel')
        self.message = MockMessage(self.author, self.channel, None)
        self.assertEqual(message_validator.channel_valid(self.message), False)