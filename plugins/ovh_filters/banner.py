#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import yaml

class Banner:
    def __init__(self, settings):
        abspath = os.path.abspath(os.path.normpath(os.path.dirname(os.curdir)))
        filename = abspath + os.sep + settings['BANNERS_FILE']
        if (os.path.isfile(filename)):
            with open(filename, 'r', encoding='utf-8') as fd:
                try:
                    self.banners = yaml.load(fd)
                except yaml.YAMLError as e:
                    logger.critical("Could not parse banners file %s. Aborting" % filepath)
                    raise e
        else:
            self.banners = dict()

    def get(self, entity):
        dir = os.path.dirname(entity.path)
        if (not self.banners or not self.banners.get(dir)):
            return None
        lang = entity.getLang()
        return self.banners.get(dir).get(lang)
