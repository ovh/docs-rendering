#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

import random

def related(entity, numberOfElements = 3):
    if not getattr(entity, 'parent', None) or not getattr(entity.parent, 'children', None):
        return []

    # get entities from the same section
    related_entities = [related_entity for related_entity in entity.parent.children if \
        getattr(related_entity, 'section', 'Misc') == getattr(entity, 'section', 'Misc') and related_entity.slug != entity.slug]

    return related_entities[:numberOfElements]
