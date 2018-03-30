#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

def breadcrumbs(entity):
    bc = [(p.title, p.url) for p in entity.parents]
    bc.append((entity.title, entity.url))
    return bc