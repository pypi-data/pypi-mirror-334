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

    async def test_determine_bet_true_gambling_true(self):
        self.message = MockMessage(self.author, self.channel, 'odds')
        self.gamble = Gamble(self.message)
        self.commandParser = CommandParser(self.message.content)
        self.commandParser.parse_init()
        self.gamble.update_gambling_state(True)
        await high_roller.handle_gamble_bet(self.gamble, self.commandParser)
        self.assertFalse(self.gamble.gambling())
        self.assertEqual(await high_roller.handle_gamble_bet(self.gamble, self.commandParser), None)

    async def test_determine_bet_true_gambling_false(self):
        self.message = MockMessage(self.author, self.channel, 'evens')
        self.gamble = Gamble(self.message)
        self.commandParser = CommandParser(self.message.content)
        self.commandParser.parse_init()
        self.gamble.update_gambling_state(False)
        await high_roller.handle_gamble_bet(self.gamble, self.commandParser)
        self.assertFalse(self.gamble.gambling())
        self.assertEqual(await high_roller.handle_gamble_bet(self.gamble, self.commandParser), None)

    async def test_determine_bet_false_gambling_true(self):
        self.message = MockMessage(self.author, self.channel, 'invalid')
        self.gamble = Gamble(self.message)
        self.commandParser = CommandParser(self.message.content)
        self.commandParser.parse_init()
        self.gamble.update_gambling_state(True)
        await high_roller.handle_gamble_bet(self.gamble, self.commandParser)
        self.assertTrue(self.gamble.gambling())
        self.assertEqual(await high_roller.handle_gamble_bet(self.gamble, self.commandParser), None)

    async def test_determine_bet_false_gambling_false(self):
        self.message = MockMessage(self.author, self.channel, 'invalid')
        self.gamble = Gamble(self.message)
        self.commandParser = CommandParser(self.message.content)
        self.commandParser.parse_init()
        self.gamble.update_gambling_state(False)
        await high_roller.handle_gamble_bet(self.gamble, self.commandParser)
        self.assertFalse(self.gamble.gambling())
        self.assertEqual(await high_roller.handle_gamble_bet(self.gamble, self.commandParser), None)