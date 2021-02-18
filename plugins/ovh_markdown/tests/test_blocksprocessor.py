#!/usr/bin/env python
import unittest
import re
import markdown
import os
from bs4 import BeautifulSoup

import sys
sys.path.append('../..')
from ovh_markdown.ovhextension import OVHMarkdownExtension


def prettify(string):
    """Prettify an html string

    Args:
        string (string): the string to prettify

    Returns:
        The prettified string
    """
    soup = BeautifulSoup(string, "html.parser")
    return soup.prettify()


class TestBlocksProcessors(unittest.TestCase):

    maxDiff = None  # Display all the diff

    test_file = 'test.md'
    expected_file = 'expected.html'

    def is_testable(self, directory):
        """Test if a directory contains the files necessary to be testable.

        Args:
            directory (string): path to test

        Returns:
            Wether the directory is testable or not.
        """
        replaceable = '{}/{}'
        return (
            os.path.isfile(replaceable.format(directory, self.test_file)) and
            os.path.isfile(replaceable.format(directory, self.expected_file))
        )

    def replace_placeholders(self, replaceable, replacer):
        """Replace placeholders

        Args:
            replaceable (string): the string containing placholder to replace
            replacer (string): the string without placeholders, used to replace

        Returns:
            Replaceable with placeholders replaced based on replacer values
        """
        split_char = '\n'
        replaceable_lines = replaceable.split(split_char)
        replacer_lines = replacer.split(split_char)

        if len(replaceable_lines) != len(replacer_lines):
            return False

        for index, line in enumerate(replaceable_lines):
            if '{}' in line:
                regex = line.replace('{}', '(.*)')
                pattern = re.compile(regex)
                replacer_line = replacer_lines[index]
                match = pattern.match(replacer_line)
                if match:
                    replaceable_lines[index] = replacer_line

        return split_char.join(replaceable_lines)


    def test_from_files(self):
        """Search for test files and run the tests.

        Run through the folders at the same level of this file and search for
        those containing both 'test.md' and 'expected.html'.

        Then run markdown using 'test.md' content as input and compare it to
        'expected.html' content.

        Both transpile result and 'expect.html' content are prettified in order
        to avoid false negatives because of formatting.
        """
        path = os.path.dirname(os.path.realpath(__file__))
        dirs = next(os.walk(path))[1]

        for directory in dirs:
            directory_path = '{}/{}'.format(path, directory)
            test_file_path = '{}/{}'.format(directory_path, self.test_file)
            expected_file_path = '{}/{}'.format(directory_path, self.expected_file)

            if self.is_testable(directory_path):
                with open(test_file_path, 'r') as test_f, open(expected_file_path, 'r') as expected_f:
                    test = test_f.read().strip()
                    expected = expected_f.read().strip()

                transpiled = markdown.markdown(
                        test,
                        extensions=[
                            'markdown.extensions.extra',
                            'mdx_include',
                            OVHMarkdownExtension({}),
                        ],
                        extension_configs={
                            'mdx_include': {
                                'base_path': directory_path
                            }
                        }
                    )

                transpiled = prettify(transpiled)
                expected = prettify(expected)

                replaced_placeholder_expected = self.replace_placeholders(expected, transpiled)
                if replaced_placeholder_expected:
                    expected = replaced_placeholder_expected

                with self.subTest(directory=directory):
                    self.assertEqual(
                        transpiled,
                        expected)


if __name__ == '__main__':
    unittest.main()
