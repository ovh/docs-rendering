#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

def visible(entities):
    return [entity for entity in entities if not getattr(entity, 'hidden', False)]