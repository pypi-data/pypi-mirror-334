import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.computing.compute import Compute
import unittest

class TestRollKhDie(unittest.TestCase):
    def setUp(self):
        self.compute = Compute()

    def test_empty_string(self):
        to_roll = ''
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_0_rolls(self):
        to_roll = '0d20kh'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_0_sides(self):
        to_roll = 'd0kh'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_0_keeps(self):
        to_roll = 'd20kh0'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_too_many_keeps(self):
        to_roll = '2d20kh2'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_too_many_rolls(self):
        to_roll = '1001d20kh'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_too_many_sides(self):
        to_roll = 'd10001kh'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_two_rolls_kh(self):
        to_roll = '2d20kh'
        self.compute.cocked_odds = 0
        self.assertIn(
            self.compute.roll_die(to_roll), [
                (1,13.825),
                (2,13.825),
                (3,13.825),
                (4,13.825),
                (5,13.825),
                (6,13.825),
                (7,13.825),
                (8,13.825),
                (9,13.825),
                (10,13.825),
                (11,13.825),
                (12,13.825),
                (13,13.825),
                (14,13.825),
                (15,13.825),
                (16,13.825),
                (17,13.825),
                (18,13.825),
                (19,13.825),
                (20,13.825)
            ])
        self.assertEqual(len(self.compute.cocked_rolls), 0)

    def test_three_rolls_kh(self):
        to_roll = '3d20kh'
        self.compute.cocked_odds = 0
        self.assertIn(
            self.compute.roll_die(to_roll), [
                (1,15.4875),
                (2,15.4875),
                (3,15.4875),
                (4,15.4875),
                (5,15.4875),
                (6,15.4875),
                (7,15.4875),
                (8,15.4875),
                (9,15.4875),
                (10,15.4875),
                (11,15.4875),
                (12,15.4875),
                (13,15.4875),
                (14,15.4875),
                (15,15.4875),
                (16,15.4875),
                (17,15.4875),
                (18,15.4875),
                (19,15.4875),
                (20,15.4875)
            ])
        self.assertEqual(len(self.compute.cocked_rolls), 0)

    def test_four_rolls_kh(self):
        to_roll = '4d20kh'
        self.compute.cocked_odds = 0
        self.assertIn(
            self.compute.roll_die(to_roll), [
                (1,16.4833375),
                (2,16.4833375),
                (3,16.4833375),
                (4,16.4833375),
                (5,16.4833375),
                (6,16.4833375),
                (7,16.4833375),
                (8,16.4833375),
                (9,16.4833375),
                (10,16.4833375),
                (11,16.4833375),
                (12,16.4833375),
                (13,16.4833375),
                (14,16.4833375),
                (15,16.4833375),
                (16,16.4833375),
                (17,16.4833375),
                (18,16.4833375),
                (19,16.4833375),
                (20,16.4833375)
            ])
        self.assertEqual(len(self.compute.cocked_rolls), 0)