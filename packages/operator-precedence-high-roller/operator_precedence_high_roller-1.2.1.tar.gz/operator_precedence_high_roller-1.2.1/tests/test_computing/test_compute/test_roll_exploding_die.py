import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.computing.compute import Compute
import unittest

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.compute = Compute()

    def test_empty_string(self):
        to_roll = ''
        self.assertEqual(self.compute.roll_exploding_die(to_roll), None)

    def test_0_rolls(self):
        to_roll = '0e20'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_0_sides(self):
        to_roll = 'e0'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_1_sided_exploding_die(self):
        to_roll = 'e1'
        self.assertEqual(self.compute.roll_exploding_die(to_roll), (1,1))

    def test_too_many_rolls(self):
        to_roll = '1001e20'
        self.assertEqual(self.compute.roll_die(to_roll), None)

    def test_too_many_sides(self):
        to_roll = 'e10001'
        self.assertEqual(self.compute.roll_die(to_roll), None)