import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.computing.compute import Compute
import unittest

class TestRollRegularDie(unittest.TestCase):
    def setUp(self):
        self.compute = Compute()

    def test_empty_string(self):
        to_roll = ''
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_0_rolls(self):
        to_roll = '0d20'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_0_sides(self):
        to_roll = 'd0'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_too_many_rolls(self):
        to_roll = '1001d20'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_too_many_sides(self):
        to_roll = 'd10001'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_one_roll(self):
        to_roll = 'd20'
        self.compute.cocked_odds = 0
        self.assertIn(
            self.compute.roll_die(to_roll), [
                (1,10),
                (2,10),
                (3,10),
                (4,10),
                (5,10),
                (6,10),
                (7,10),
                (8,10),
                (9,10),
                (10,10),
                (11,10),
                (12,10),
                (13,10),
                (14,10),
                (15,10),
                (16,10),
                (17,10),
                (18,10),
                (19,10),
                (20,10)
            ])
        self.assertEqual(len(self.compute.cocked_rolls), 0)
        
    def test_two_rolls(self):
        to_roll = '2d6'
        self.compute.cocked_odds = 0
        self.assertIn(
            self.compute.roll_die(to_roll), [
                (2, 7),
                (3, 7),
                (4, 7),
                (5, 7),
                (6, 7),
                (7, 7),
                (8, 7),
                (9, 7),
                (10, 7),
                (11, 7),
                (12, 7)
            ])
        self.assertEqual(len(self.compute.cocked_rolls), 0)

    def test_one_roll_cocked(self):
        to_roll = 'd20'
        self.compute.cocked_odds = 1
        self.assertIn(
            self.compute.roll_die(to_roll), [
                (1,10),
                (2,10),
                (3,10),
                (4,10),
                (5,10),
                (6,10),
                (7,10),
                (8,10),
                (9,10),
                (10,10),
                (11,10),
                (12,10),
                (13,10),
                (14,10),
                (15,10),
                (16,10),
                (17,10),
                (18,10),
                (19,10),
                (20,10)
            ])
        self.assertEqual(len(self.compute.cocked_rolls), 1)
        
    def test_two_rolls_cocked(self):
        to_roll = '2d6'
        self.compute.cocked_odds = 1
        self.assertIn(
            self.compute.roll_die(to_roll), [
                (2, 7),
                (3, 7),
                (4, 7),
                (5, 7),
                (6, 7),
                (7, 7),
                (8, 7),
                (9, 7),
                (10, 7),
                (11, 7),
                (12, 7)
            ])
        self.assertEqual(len(self.compute.cocked_rolls), 2)

    def test_two_rolls_kh(self):
        to_roll = '2d6kh'
        self.compute.cocked_odds = 0
        self.assertIn(
            self.compute.roll_die(to_roll), [
                (1, 4.472222222222222),
                (2, 4.472222222222222),
                (3, 4.472222222222222),
                (4, 4.472222222222222),
                (5, 4.472222222222222),
                (6, 4.472222222222222)
            ])
        self.assertEqual(len(self.compute.cocked_rolls), 0)

    """def test_three_rolls_kh2(self):
        to_roll = '3d6kh2'
        self.compute.cocked_odds = 0
        self.assertIn(
            self.compute.roll_die(to_roll), [
                (1, 4.472222222222222),
                (2, 4.472222222222222),
                (3, 4.472222222222222),
                (4, 4.472222222222222),
                (5, 4.472222222222222),
                (6, 4.472222222222222)
            ])
        self.assertEqual(len(self.compute.cocked_rolls), 0)"""