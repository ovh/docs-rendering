#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

import os
import yaml

class Translator:
    def __init__(self, settings):
        abspath = os.path.abspath(os.path.normpath(os.path.dirname(os.curdir)))
        filename = abspath + os.sep + settings['TRANSLATIONS_FILE']
        if (os.path.isfile(filename)):
            with open(filename, 'r', encoding='utf-8') as fd:
                try:
                    self.translations = yaml.load(fd)
                except yaml.YAMLError as e:
                    logger.critical("Could not parse translation file %s. Aborting" % filepath)
                    raise e
        else:
            self.translations = dict()

    def translate(self, string, lang):
        if not self.translations.get(string):
            return string
        elif not self.translations.get(string).get(lang):
            return string
        else:
            return self.translations.get(string).get(lang)