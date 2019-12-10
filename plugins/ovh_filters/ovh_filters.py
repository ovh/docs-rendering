#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from pelican import signals
from .translator import Translator
from .banner import Banner
from .breadcrumbs import breadcrumbs
from .related import related
from .visible import visible

def add_filter(generator):
    translator = Translator(generator.settings)
    generator.env.filters.update({'translate': translator.translate})
    banner = Banner(generator.settings)
    generator.env.filters.update({'banner': banner.get})
    generator.env.filters.update({'breadcrumbs': breadcrumbs})
    generator.env.filters.update({'related': related})
    generator.env.filters.update({'visible': visible})

def register():
    """Plugin registration."""
    signals.generator_init.connect(add_filter)
