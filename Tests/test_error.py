#!/usr/bin/python

import unittest
import xml.etree.ElementTree as ET
from subprocess import PIPE, STDOUT, Popen


class ErrorTests(unittest.TestCase):
    def validate_error(self, tex_input, error_id, start_position, length):
        p = Popen(
            ['../blahtex', '--mathml'],
            stdout=PIPE,
            stdin=PIPE,
            stderr=STDOUT
        )

        p.stdin.write(tex_input.encode())
        p.stdin.close()
        p.wait()

        error_node = ET.fromstring(p.stdout.read())

        self.assertEqual(error_node.find("id").text, error_id)
        self.assertEqual(int(error_node.find("startPos").text), start_position)
        self.assertEqual(int(error_node.find("length").text), length)


class BraceErrorTests(ErrorTests):
    def test_open_brace(self):
        self.validate_error("2^{5", "UnmatchedOpenBrace", 2, 1)
        self.validate_error("4^{6 * 2^{5", "UnmatchedOpenBrace", 9, 1)
        self.validate_error("4^{6} * 2^{5", "UnmatchedOpenBrace", 10, 1)
        self.validate_error("2^{2{5}", "UnmatchedOpenBrace", 4, 1)

    def test_close_brace(self):
        self.validate_error("2^5}", "UnmatchedCloseBrace", 3, 1)


class CharErrorTests(ErrorTests):
    def test_illegal_final_backslash(self):
        self.validate_error("2\\", "IllegalFinalBackslash", 1, 1)


class RecognitionErrorTests(ErrorTests):
    def test_unrecognised_command(self):
        self.validate_error(
            "2 + \\testingwrongcommand", "UnrecognisedCommand", 4, 20
        )


if __name__ == '__main__':
    unittest.main()
