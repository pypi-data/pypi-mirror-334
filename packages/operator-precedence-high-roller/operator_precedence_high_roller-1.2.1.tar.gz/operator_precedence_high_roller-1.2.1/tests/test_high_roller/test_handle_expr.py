import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, ''))
import high_roller
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from operator_precedence_high_roller.computing.compute import Compute
from operator_precedence_high_roller.json_handling.roll_saving.roll_save import RollSave
from tests.mock_classes.mock_message_attributes.mock_author import MockAuthor
from tests.mock_classes.mock_message_attributes.mock_channel import MockChannel
from tests.mock_classes.mock_message import MockMessage
from unittest import IsolatedAsyncioTestCase
from mock import patch

class TestHandleExpr(IsolatedAsyncioTestCase):
    def setUp(self):
        self.author = MockAuthor(name = 'test_1234')
        self.channel = MockChannel(name = 'rolls_test_1234')
        self.compute = Compute()

    async def test_parse_error(self):
        self.message = MockMessage(self.author, self.channel, '!x')
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        with patch.object(high_roller, 'handle_error') as mock:
            await high_roller.handle_expr(self.message, self.compute, self.rollSave, self.commandParser)
        mock.assert_called_with(self.message)
        self.assertEqual(await high_roller.handle_expr(self.message, self.compute, self.rollSave, self.commandParser), None)

    async def test_compute_error(self):
        self.message = MockMessage(self.author, self.channel, '!d20/0')
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        with patch.object(high_roller, 'handle_error') as mock:
            await high_roller.handle_expr(self.message, self.compute, self.rollSave, self.commandParser)
        mock.assert_called_with(self.message)
        self.assertEqual(await high_roller.handle_expr(self.message, self.compute, self.rollSave, self.commandParser), None)

    async def test_message_too_long(self):
        self.message = MockMessage(self.author, self.channel, '!1000d1000')
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        with patch.object(high_roller, 'handle_error') as mock:
            await high_roller.handle_expr(self.message, self.compute, self.rollSave, self.commandParser)
        mock.assert_called_with(self.message)
        self.assertEqual(await high_roller.handle_expr(self.message, self.compute, self.rollSave, self.commandParser), None)

    async def test_no_cocked_rolls(self):
        self.message = MockMessage(self.author, self.channel, '!d1')
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        self.compute.cocked_odds = 0
        with patch.object(self.message.channel, 'send') as mock:
            await high_roller.handle_expr(self.message, self.compute, self.rollSave, self.commandParser)
        mock.assert_called_with('1\nDetails: ' + str(self.compute.all_lists_of_rolls) + '\nAverage: 1')
        self.assertEqual(await high_roller.handle_expr(self.message, self.compute, self.rollSave, self.commandParser), None)

    async def test_1_cocked_roll(self):
        self.message = MockMessage(self.author, self.channel, '!d1')
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content.lower())
        self.commandParser.parse_init()
        self.compute.cocked_odds = 1
        with patch.object(self.message.channel, 'send') as mock:
            await high_roller.handle_expr(self.message, self.compute, self.rollSave, self.commandParser)
        mock.assert_called_with('Honor the cock. Roll 1 was cocked. It would have been 1\n1\nDetails: ' + str(self.compute.all_lists_of_rolls) + '\nAverage: 1')
        self.assertEqual(await high_roller.handle_expr(self.message, self.compute, self.rollSave, self.commandParser), None)