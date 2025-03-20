import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, ''))
import high_roller
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from operator_precedence_high_roller.computing.compute import Compute
from operator_precedence_high_roller.json_handling.gambling.gamble import Gamble
from operator_precedence_high_roller.json_handling.roll_saving.roll_save import RollSave
from tests.mock_classes.mock_message_attributes.mock_author import MockAuthor
from tests.mock_classes.mock_message_attributes.mock_channel import MockChannel
from tests.mock_classes.mock_message import MockMessage
from unittest import IsolatedAsyncioTestCase
from mock import patch

class TestHandleExpr(IsolatedAsyncioTestCase):
    def setUp(self):
        self.author = MockAuthor(name = 'test_1234')
        self.compute = Compute()

    async def test_invalid_channel_valid_command(self):
        self.channel = MockChannel(name = 'invalid_channel')
        self.message = MockMessage(self.author, self.channel, '!d20')
        self.gamble = Gamble(self.message)
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        with patch.object(high_roller, 'handle_error') as mock:
            await high_roller.on_message(self.message)
        mock.assert_called_with(self.message)

    async def test_invalid_command(self):
        self.channel = MockChannel(name = 'rolls_test_1234')
        self.message = MockMessage(self.author, self.channel, 'this is not a valid command')
        self.gamble = Gamble(self.message)
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        with patch.object(high_roller, 'handle_error') as mock:
            await high_roller.on_message(self.message)
        mock.assert_not_awaited()

    async def test_await_handle_expr(self):
        self.channel = MockChannel(name = 'rolls_test_1234')
        self.message = MockMessage(self.author, self.channel, '!d20+(3d6-2d4)/2')
        self.gamble = Gamble(self.message)
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        with patch.object(high_roller, 'handle_expr') as mock:
            await high_roller.on_message(self.message)
        mock.assert_called()
        self.assertEqual(await high_roller.on_message(self.message), None)

    async def test_await_handle_gamble_start(self):
        self.channel = MockChannel(name = 'rolls_test_1234')
        self.message = MockMessage(self.author, self.channel, '!gamble')
        self.gamble = Gamble(self.message)
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        with patch.object(high_roller, 'handle_gamble_start') as mock:
            await high_roller.on_message(self.message)
        mock.assert_called()
        self.assertEqual(await high_roller.on_message(self.message), None)

    async def test_await_handle_gamble_bet(self):
        self.channel = MockChannel(name = 'rolls_test_1234')
        self.message = MockMessage(self.author, self.channel, 'odds')
        self.gamble = Gamble(self.message)
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        with patch.object(high_roller, 'handle_gamble_bet') as mock:
            await high_roller.on_message(self.message)
        mock.assert_called()
        self.assertEqual(await high_roller.on_message(self.message), None)

    async def test_await_handle_recall_rolls(self):
        self.channel = MockChannel(name = 'rolls_test_1234')
        self.message = MockMessage(self.author, self.channel, '!h')
        self.gamble = Gamble(self.message)
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        with patch.object(high_roller, 'handle_recall_rolls') as mock:
            await high_roller.on_message(self.message)
        mock.assert_called()
        self.assertEqual(await high_roller.on_message(self.message), None)