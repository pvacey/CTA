#!/usr/bin/env python

import unittest
import cta

class TestCTAMethods(unittest.TestCase):
    def setUp(self):
        self.lines = cta.get_lines()

    def test_linesExist(self):
        self.assertIsNotNone(self.lines)

    def test_brownLine(self):
        self.assertEqual(self.lines['brown'], 'Brn')

    def test_pinkLine(self):
        self.assertEqual(self.lines['pink'], 'Pnk')

    def test_greenLine(self):
        self.assertEqual(self.lines['green'], 'G')

    def test_yellowLine(self):
        self.assertEqual(self.lines['yellow'], 'Y')

    def test_blueLine(self):
        self.assertEqual(self.lines['blue'], 'Blue')

if __name__ == '__main__':
    unittest.main()
