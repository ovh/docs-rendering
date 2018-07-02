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
