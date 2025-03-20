import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, ''))
import high_roller
from operator_precedence_high_roller.json_handling.gambling.gamble import Gamble
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from tests.mock_classes.mock_message_attributes.mock_author import MockAuthor
from tests.mock_classes.mock_message_attributes.mock_channel import MockChannel
from tests.mock_classes.mock_message import MockMessage
from unittest import IsolatedAsyncioTestCase

class TestHandleGambleStart(IsolatedAsyncioTestCase):
    def setUp(self):
        self.author = MockAuthor(name = 'test_1234')
        self.channel = MockChannel(name = 'rolls_test_1234')
        self.message = MockMessage(self.author, self.channel, '!gamble')
        self.gamble = Gamble(self.message)
        self.commandParser = CommandParser(self.message.content)
        self.commandParser.parse_init()

    async def test_not_gambling_true(self):
        self.gamble.update_gambling_state(False)
        await high_roller.handle_gamble_start(self.message, self.gamble)
        self.assertTrue(self.gamble.gambling())
        self.assertEqual(await high_roller.handle_gamble_start(self.message, self.gamble), None)

    async def test_not_gambling_false(self):
        self.gamble.update_gambling_state(True)
        await high_roller.handle_gamble_start(self.message, self.gamble)
        self.assertTrue(self.gamble.gambling())
        self.assertEqual(await high_roller.handle_gamble_start(self.message, self.gamble), None)