#!/usr/bin/env python

import unittest
import cta

class TestCTAMethods(unittest.TestCase):
    def setUp(self):
        self.lines = cta.getLines()

    def test_linesExist(self):
        self.assertIsNotNone(self.lines)

    def test_brownLine(self):
        self.assertEqual(self.lines['Brn'], 'Brown')

    def test_pinkLine(self):
        self.assertEqual(self.lines['Pnk'], 'Pink')

    def test_greenLine(self):
        self.assertEqual(self.lines['G'], 'Green')

    def test_yellowLine(self):
        self.assertEqual(self.lines['Y'], 'Yellow')

if __name__ == '__main__':
    unittest.main()
