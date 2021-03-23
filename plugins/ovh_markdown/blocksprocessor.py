#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import re
import sys, traceback
import collections
import uuid

from markdown.blockprocessors import BlockProcessor
from markdown import util

class DefaultBlockProcessor(BlockProcessor):

    def __init__(self, parser, extension, re_follow=r"\>[ ]?(.*)"):
        super(DefaultBlockProcessor, self).__init__(parser)
        self.extension = extension
        self.re_follow = re.compile(re_follow)

    def clean(self, line):
        """ Remove ``>`` from beginning of a line. """
        m = self.re_follow.match(line)
        if line.strip() == ">":
            return ""
        elif m:
            return m.group(1)
        else:
            return line

class BlockCalloutProcessor(DefaultBlockProcessor):
    RE = re.compile(r"(^|\n)\>[ ]?\[\!(alert|warning|hint|note|primary|success|secondary)\]")

    def __init__(self, parser, extension):
        super(BlockCalloutProcessor, self).__init__(parser, extension)

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            css_class = m.group(2)
            before = block[:m.start()]
            self.parser.parseBlocks(parent, [before])
            block = '\n'.join(
                [self.clean(line) for line in block[m.start():].split('\n')][1:]
            )

        div = util.etree.SubElement(parent, 'div')
        div.attrib = { 'class': 'callout {}'.format(css_class) }

        self.parser.state.set('div')
        self.parser.parseChunk(div, block)
        self.parser.state.reset()

class BlockProductSectionProcessor(DefaultBlockProcessor):
    RE = re.compile(r"(^|\n)\>[ ]?\[\!product-section(\((?P<side>left|right)\)){0,1}\]")

    def __init__(self, parser, extension):
        super(BlockProductSectionProcessor, self).__init__(parser, extension)

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            side = 'right' if m.group('side') == 'right' else 'left'
            before = block[:m.start()]
            self.parser.parseBlocks(parent, [before])
            block = '\n'.join(
                [self.clean(line) for line in block[m.start():].split('\n')][1:]
            )

        div = util.etree.SubElement(parent, 'div')
        div.attrib = { 'class': 'columns large-6 medium-6 small-12 product-section ' + side }

        column = util.etree.SubElement(div, 'div')
        column.attrib = { 'class': 'columns' }

        self.parser.state.set('div')
        self.parser.parseChunk(column, block)
        self.parser.state.reset()

class BlockApiProcessor(DefaultBlockProcessor):
    RE = re.compile(r"(^|\n)\>[ ]?\[\!(api)\]")
    RE_API = re.compile(r"^@api(\((?P<zone>.*)\))? \{(?P<method>\w+)\} (?P<endpoint>.+)")

    def __init__(self, parser, extension):
        super(BlockApiProcessor, self).__init__(parser, extension)

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            css_class = m.group(2)
            before = block[:m.start()]
            self.parser.parseBlocks(parent, [before])
            lines = [self.clean(line) for line in block[m.start():].split('\n')][1:]


        div = util.etree.SubElement(parent, 'div')
        div.attrib = { 'class': 'ovh-api' }

        for line in lines:
            if line:
                m = self.RE_API.match(line)
                if m:
                    zone = m.group('zone')
                    method = m.group('method')
                    endpoint = m.group('endpoint')

                    block = """<div class="ovh-api-main">
                                   <a target="_blank" href="https://eu.api.ovh.com/console/#{0}#{1}">
                                       <span class="ovh-api-verb ovh-api-verb-{1}">{2}</span>
                                       <span class="ovh-api-endpoint">{0}</span></a>
                                </div>""".format(endpoint, method.upper(), method)

                    self.parser.state.set('div')
                    self.parser.parseChunk(div, block)
                    self.parser.state.reset()

class BlockCarouselProcessor(DefaultBlockProcessor):
    RE = re.compile(r"(^|\n)\>[ ]?\[\!carousel\]")
    RE_IMG = re.compile(r"\-[ ]?!\[(?P<alt>.*)\]\((?P<src>.*)\)([ ](?P<caption>.+))?")

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            before = block[:m.start()]
            self.parser.parseBlocks(parent, [before])
            lines = [self.clean(line) for line in block[m.start():].split('\n')][1:]

        root = util.etree.SubElement(parent, 'div')
        root.attrib = { 'class': 'carousel' }

        for line in lines:
            m = self.RE_IMG.match(line)
            if m:
                alt = m.group('alt')
                src = m.group('src')
                caption = m.group('caption')
                div = util.etree.SubElement(root, 'div')

                img = util.etree.SubElement(div, 'img')
                img.attrib = { 'class': 'carousel-image', 'alt': alt, 'src': src }

                fc = util.etree.SubElement(div, 'figcaption')
                fc.attrib = { 'class': 'carousel-caption' }
                fc.text = caption if caption else alt

class BlockFaqProcessor(DefaultBlockProcessor):
    RE = re.compile(r"(^|\n)\>[ ]?\[\!faq\]")

    def __init__(self, parser, extension):
        super(BlockFaqProcessor, self).__init__(parser, extension)

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            before = block[:m.start()]
            self.parser.parseBlocks(parent, [before])
            lines = [self.clean(line) for line in block[m.start():].split('\n')][1:]

        dl = util.etree.SubElement(parent, 'dl')
        dl.attrib = { 'class': 'docutils' }

        try:
            self.parse_lines(dl, lines)
        except Exception as e:
            ex_type, ex, tb = sys.exc_info()
            traceback.print_tb(tb)
            del tb


    def append_questions(self, element, questions):
        for q, v in questions:
            dt = util.etree.SubElement(element, 'dt')
            dt.text = '<em>%s</em>' % q

            answer = []

            for item in v:
                if isinstance(item, str):
                    answer.append(item)
                else:
                    self.append_answer_and_table(element, answer, item)
                    answer = []

            self.append_answer_and_table(element, answer, [])

    def append_answer_and_table(self, element, answer, table):
        if len(answer):
            dd = util.etree.SubElement(element, 'dd')
            self.parser.parseChunk(dd, '\n'.join(answer))

        if len(table):
            dd = util.etree.SubElement(element, 'dd')
            t = util.etree.SubElement(dd, 'table')
            t.attrib = {'class': 'first last docutils field-list'}

            for (name, body) in table:
                tr = util.etree.SubElement(t, 'tr')
                tr.attrib = {'class': 'field'}

                th = util.etree.SubElement(tr, 'th')
                th.attrib = {'class': 'field-name'}
                th.text = name

                td = util.etree.SubElement(tr, 'td')
                td.attrib = {'class': 'field-body'}
                self.parser.parseChunk(td, '\n'.join([l for l in body]))

    def parse_lines(self, element, lines):
        questions = []

        try:
            for line in lines:
                if line:
                    if line[0] != '>':
                        questions.append((line, []))
                    elif line[0:2] == '> ':
                        if len(questions[-1][-1]) > 0 and isinstance(questions[-1][-1][-1], str):
                            s = questions[-1][-1][-1]
                            if s == '' or s[0].isalpha():
                                questions[-1][-1][-1] = questions[-1][-1][-1] + '\n'
                        questions[-1][-1].append(line[2:])
                    elif line[0:2] == '>>':
                        if len(questions[-1][-1]) > 1 and isinstance(questions[-1][-1][-2], list):
                            questions[-1][-1][-2].append((questions[-1][-1].pop(), []))
                        elif len(questions[-1][-1]) > 0 and isinstance(questions[-1][-1][-1], str):
                            questions[-1][-1][-1] = [(questions[-1][-1][-1], [])]
                        questions[-1][-1][-1][-1][-1].append(line[2:].strip())
                    else:
                        questions[-1][-1].append('')

        except Exception as e:
            ex_type, ex, tb = sys.exc_info()
            traceback.print_tb(tb)
            del tb

        self.append_questions(element, questions)

        self.parser.state.set('dl')
        self.parser.state.reset()


class BlockTabsProcessor(DefaultBlockProcessor):
    RE = re.compile(r"(^|\n)\>[ ]?\[\!tabs\]")

    def __init__(self, parser, extension):
        super(BlockTabsProcessor, self).__init__(parser, extension)

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def build_tabs_object(self, lines):
        tabs = collections.OrderedDict()
        currentTitle = None

        for line in lines:
            if line[0] != ">":
                currentTitle = line
                if currentTitle not in tabs:
                    tabs[currentTitle] = []
            elif line[0] == ">" and currentTitle is not None:
                tabs[currentTitle].append(self.clean(line))

        return tabs

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            before = block[:m.start()]
            self.parser.parseBlocks(parent, [before])
            lines = [self.clean(line) for line in
                    block[m.start():].split('\n')][1:]
        else:
            lines = []

        if lines:
            try:
                tabs = self.build_tabs_object(lines)
                uid = uuid.uuid1()

                # main div
                root = util.etree.SubElement(parent, 'div')
                root.attrib = { 'class': 'ovh__tabs' }

                # tabs titles
                titles = util.etree.SubElement(root, 'ul')
                titles.attrib = {
                    'class': 'tabs',
                    'data-tabs': '',
                    'id': 'collapsing-tabs-{}'.format(uid)
                }

                # tabs content
                content = util.etree.SubElement(root, 'div')
                content.attrib = {
                    'class': 'tabs-content',
                    'data-tabs-content': 'collapsing-tabs-{}'.format(uid)
                }

                for index, tab in enumerate(tabs):
                    is_active = index == 0
                    panel = 'panel-{}-{}'.format(uid, index)

                    # append titles
                    titles_li = util.etree.SubElement(titles, 'li')
                    titles_li.attrib = {
                        'class': 'tabs-title' +
                            (' is-active' if is_active else '')
                    }

                    link = util.etree.SubElement(titles_li, 'a')
                    link.attrib = {
                        'href': '#{}'.format(panel)
                    }

                    if index == 0:
                        link.attrib['aria-selected'] = 'true'

                    link.text = tab

                    # append content
                    children = tabs[tab]

                    wrapper = util.etree.SubElement(content, 'div')
                    wrapper.attrib = {
                        'class': 'tabs-panel' +
                            (' is-active' if is_active else ''),
                        'id': '{}'.format(panel)
                    }

                    # run preprocessors on tabs content
                    for prep in self.parser.markdown.preprocessors.values():
                        children = prep.run(children)

                    self.parser.parseChunk(wrapper, '\n'.join(children))

            except Exception as e:
                ex_type, ex, tb = sys.exc_info()
                del ex_type, ex
                traceback.print_tb(tb)

