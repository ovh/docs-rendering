#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from markdown.extensions import Extension
from .blocksprocessor import BlockCalloutProcessor, BlockApiProcessor, BlockFaqProcessor, BlockCarouselProcessor, BlockProductSectionProcessor
from .preprocessor import NormalizeImg, NormalizeLink


class OVHMarkdownExtension(Extension):

    def __init__(self, config):
        try:
            # Needed for Markdown versions >= 2.5
            self.config['config'] = ['{}', 'config for markdown extension']
            super(OVHMarkdownExtension, self).__init__(**config)
        except AttributeError:
            # Markdown versions < 2.5
            config['config'] = [config['config'], 'config for markdown extension']
            super(OVHMarkdownExtension, self).__init__(config)

    def extendMarkdown(self, md, md_globals):
        # Add preprocessors 
        md.preprocessors.add(
            'normalize_img', NormalizeImg(md), '>reference'
        )
        md.preprocessors.add(
            'normalize_link', NormalizeLink(md), '>normalize_img'
        )

        # Add blockprocessors 
        md.parser.blockprocessors.add(
            'product_section', BlockProductSectionProcessor(md.parser, self), '>ulist'
        )
        md.parser.blockprocessors.add(
            'callout', BlockCalloutProcessor(md.parser, self), '>product_section'
        )
        md.parser.blockprocessors.add(
            'api', BlockApiProcessor(md.parser, self), '>callout'
        )
        md.parser.blockprocessors.add(
            'carousel', BlockCarouselProcessor(md.parser, self), '>api'
        )
        md.parser.blockprocessors.add(
            'faq', BlockFaqProcessor(md.parser, self), '>carousel'
        )

        md.registerExtension(self)
