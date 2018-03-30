#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import os
import sys

from pelican import signals

try:
    from .ovhextension import OVHMarkdownExtension
except ImportError as e:
    OVHMarkdownExtension = None
    print(e.message)
    print("\nMarkdown is not installed - OVH Markdown extension disabled\n")

def process_settings(pelicanobj):
    """Sets user specified settings (see README for more details)"""

    # Default settings
    ovh_settings = {}
    ovh_settings['config'] = {}

    # Get the user specified settings
    try:
        settings = pelicanobj.settings['MD_OVH']
    except:
        settings = None

    # If settings have been specified, add them to the config
    if isinstance(settings, dict):
        ovh_settings['config'].update(settings)

    return ovh_settings

def ovh_markdown_extension(pelicanobj, config):
    """Instantiates a customized Markdown extension"""

    # Instantiate Markdown extension and append it to the current extensions
    try:
        pelicanobj.settings['MARKDOWN']['extensions'].append(OVHMarkdownExtension(config))
        
    except:
        sys.excepthook(*sys.exc_info())
        sys.stderr.write("\nError - the pelican Markdown extension failed to configure. OVH Markdown extension is non-functional.\n")
        sys.stderr.flush()

def ovh_init(pelicanobj):
    """Loads settings and instantiates the Python Markdown extension"""

    # If there was an error loading Markdown, then do not process any further 
    if not OVHMarkdownExtension:
        return

    # Process settings
    config = process_settings(pelicanobj)

    # Configure Markdown Extension
    ovh_markdown_extension(pelicanobj, config)

def register():
    """Plugin registration"""
    signals.initialized.connect(ovh_init)