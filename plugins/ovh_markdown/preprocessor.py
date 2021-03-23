#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import re

from markdown.preprocessors import Preprocessor

class NormalizeImg(Preprocessor):
    """ add forgotten {attach}. """

    def run(self, lines):
        source = '\n'.join(lines)
        source = re.sub(r'\!\[([^\]]*)\]\(images\/([^)]*)\)', '![\g<1>]({attach}images/\g<2>)', source)
        return source.split('\n')

class NormalizeLink(Preprocessor):
    """ add forgotten {filename}. """

    def run(self, lines):
        source = '\n'.join(lines)
        source = re.sub(r'\[(.*)\]\((.*\.md)\)', '[\g<1>]({filename}\g<2>)', source)
        return source.split('\n')

class TabsPreprocessor(Preprocessor):
    """ preprocess tabs charactes in tabs component """

    def prepend_tab_char(self, line):
        TAB_CHAR_RE = re.compile(r">>[ ]?(?P<content>[\t]+.*)")
        content_match = TAB_CHAR_RE.match(line)

        if content_match:
            line = "{}\t{}".format('>>', content_match.group('content'))

        return line

    def is_in_tabs_component(self, line, in_tabs):
        TABS_RE = re.compile(r"(^|\n)\>[ ]?\[\!tabs\]")
        if bool(TABS_RE.match(line)):
            in_tabs = True
        elif in_tabs and not line.startswith('>'):
            in_tabs = False

        return in_tabs

    def run(self, lines):
        in_tabs = False
        altered_lines = []

        for line in lines:
            in_tabs = self.is_in_tabs_component(line, in_tabs)

            if in_tabs:
                line = self.prepend_tab_char(line)

            altered_lines.append(line)

        return altered_lines
