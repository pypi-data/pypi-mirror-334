import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, ''))
import high_roller
from operator_precedence_high_roller.json_handling.gambling.gamble import Gamble
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from operator_precedence_high_roller.computing.compute import Compute
from operator_precedence_high_roller.json_handling.roll_saving.roll_save import RollSave
from tests.mock_classes.mock_message_attributes.mock_author import MockAuthor
from tests.mock_classes.mock_message_attributes.mock_channel import MockChannel
from tests.mock_classes.mock_message import MockMessage
from unittest import IsolatedAsyncioTestCase
from mock import patch

class TestHandleRecallRolls(IsolatedAsyncioTestCase):
    def setUp(self):
        self.author = MockAuthor(name = 'jaderton')
        self.channel = MockChannel(name = 'rolls_test_1234')

    async def test_basic_recall(self):
        self.message = MockMessage(self.author, self.channel, '!h')
        self.compute = Compute()
        self.gamble = Gamble(self.message)
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content)
        self.commandParser.parse_init()
        with patch.object(self.rollSave, 'get_rolls_from_json') as mock:
            await high_roller.handle_recall_rolls(self.message, self.rollSave, self.commandParser)
        mock.assert_called_with()
        self.assertEqual(await high_roller.handle_recall_rolls(self.message, self.rollSave, self.commandParser), None)

    async def test_specific_input_recall(self):
        self.message = MockMessage(self.author, self.channel, '!h(24, d20)')
        self.compute = Compute()
        self.gamble = Gamble(self.message)
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content)
        self.commandParser.parse_init()
        with patch.object(self.rollSave, 'get_rolls_from_json') as mock:
            await high_roller.handle_recall_rolls(self.message, self.rollSave, self.commandParser)
        mock.assert_called_with(hours = 24, die = 'd20')
        self.assertEqual(await high_roller.handle_recall_rolls(self.message, self.rollSave, self.commandParser), None)

    async def test_invalid_recall_message(self):
        self.message = MockMessage(self.author, self.channel, '!hh')
        self.compute = Compute()
        self.gamble = Gamble(self.message)
        self.rollSave = RollSave(self.message, self.compute)
        self.commandParser = CommandParser(self.message.content)
        self.commandParser.parse_init()
        with patch.object(high_roller, 'handle_error') as mock:
            await high_roller.handle_recall_rolls(self.message, self.rollSave, self.commandParser)
        mock.assert_called_with(self.message)
        self.assertEqual(await high_roller.handle_recall_rolls(self.message, self.rollSave, self.commandParser), None)