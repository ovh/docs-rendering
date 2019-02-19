#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import glob
import logging
import os
import re
import sys

from blinker import signal
from entities import Entity, EntityFactory, EntityGenerator, entity_subgenerator_pretaxonomy, entity_generator_finalized, entity_writer_finalized
from itertools import groupby
from operator import attrgetter
from collections import defaultdict, OrderedDict

import pelican.contents as contents
from pelican import signals

logger = logging.getLogger(__name__)

ovh_entity_subgenerator_preread = signal('entity_subgenerator_preread')
ovh_entity_subgenerator_context = signal('entity_subgenerator_context')

def process_translations(content_list, default_lang='fr-fr'):
    content_list.sort(key=attrgetter('source_path'))
    grouped_by_paths = groupby(
            content_list,
            lambda content: os.path.dirname(content.source_path))
    index = []
    translations = []

    for path, items in grouped_by_paths:
        items = list(items)

        original_items = [i for i in items if i.lang == default_lang]
        if len(original_items) == 0:
            original_items = [items[0]]

        index.extend(original_items)
        translations.extend([x for x in items if x not in original_items])
        for a in items:
            a.translations = [x for x in items if x != a]

    return index, translations


def append_children(entities, all_entities):
    items = []
    for e in [e for e in all_entities if e.parent_dir == entities[0].dir and (e.type in entities[0].settings['CHILDREN'])]:
        items += [e]
        items += e.translations

    for entity in entities:
        entity.children = [item for item in items if item.getLang() == entity.getLang()]
        sections = { 'odd': OrderedDict(), 'even': OrderedDict() }
        for index, section in enumerate(entity.getSections()):
            sections['odd' if index % 2 == 0 else 'even'][section.strip()] = [child for child in entity.children if getattr(child, 'section', 'Misc') == section.strip()]
        entity.sections = sections


def handle_entity_generator_finalized(generator):
    for entity in sorted(generator.entities, key=lambda e: e.type):
        items = [entity]
        items += entity.translations
        parent = [e for e in generator.entities if e.dir == entity.parent_dir and entity.type in e.settings['CHILDREN']]
        
        if len(parent) == 0 and not entity.settings['IS_ROOT']:
            logger.warning("No parent found for file %s", entity.source_path)

        for item in items:
            item.parent = parent[0] if len(parent) > 0 else None

        append_children(items, generator.entities)


def get_generators(pelican_object):
    return OvhEntityGenerator


def handle_entity_writer_finalized(generator, writer):
    if 'ENTITY_TYPES' in generator.settings:
        items = []
        for key in generator.settings['ENTITY_TYPES']:
            entities = [e for e in generator.entities if e.type == key]
            items.append('{} {}(s)'.format(len(entities), key))

        print('Done: Processed {}'.format(', '.join(items)))


def register():
    signals.get_generators.connect(get_generators)
    entity_generator_finalized.connect(handle_entity_generator_finalized)
    entity_writer_finalized.connect(handle_entity_writer_finalized)


def get_default_ovh_entity_settings():
    settings = {}

    settings["CHILDREN"] = []
    settings['EXCLUDE_SLUGS'] = []
    settings['SKIP_SLUG'] = False
    settings['IS_ROOT'] = False

    return settings

class OvhEntity(Entity):
    def __init__(self, content, metadata=None, settings=None, source_path=None, context=None):
        entity_settings = get_default_ovh_entity_settings()
        entity_settings.update(settings)

        super(OvhEntity, self).__init__(content, metadata, entity_settings, source_path, context)

        self.dir, filename = os.path.split(os.path.relpath(source_path))
        self.parent_dir = os.sep.join(self.dir.split(os.sep)[0:-1])

    @property
    def parents(self):
        if hasattr(self, '_parents'):
            return self._parents

        self._parents = []

        e = self
        while hasattr(e, 'parent') and e.parent:
            lang, parent_lang = e.getLang(), e.parent.getLang()
            if lang != parent_lang:
                parents_found = [t for t in e.parent.translations if t.getLang() == lang]
                if len(parents_found) > 0:
                    e.parent = parents_found[0]
                
            self._parents.insert(0, e.parent)
            e = e.parent

        return self._parents

    @property
    def url(self):
        return self.override_url

    @property
    def override_url(self):
        if hasattr(self, '_override_url'):
            return self._override_url

        slugs = [p.slug for p in self.parents if p.type not in self.settings['EXCLUDE_SLUGS']]
        g = self.metadata['global']
        l = self.metadata['locale']

        if not self.settings['SKIP_SLUG'] and self.slug:
            slugs.append(self.slug)

        generated_url = (g + '/' if g == l else g + '/' + l + '/') + '/'.join(slugs)

        if generated_url[-1] != '/':
            generated_url = generated_url + '/'

        self._override_url = generated_url

        return self._override_url
    
    @property
    def override_save_as(self):
        return self.override_url + 'index.html'

    @property
    def path(self):
        return os.path.relpath(self.source_path, self.settings['PATH'] + '/..')

    def getSections(self):
        sections = [name.strip() for name in getattr(self, 'sections', 'Misc').split(',')]
        sections += list(set([getattr(child, 'section', 'Misc').strip() for child in self.children]) - set(sections))
        return sections

    def _get_content(self):
        content = self._content

        instrasite_link_regex = self.settings['INTRASITE_LINK_REGEX']
        regex = r"""
            (?P<markup><[^\>]+  # match tag with all url-value attributes
                (?:href)\s*=\s*)
            (?P<quote>["\'])      # require value to be quoted
            (?P<path>{0}(?P<value>.*?))  # the url value
            \2>(?P<text>.*?)<""".format(instrasite_link_regex)
        hrefs = re.compile(regex, re.X)

        def replacer(m):
            markup = m.group('markup')
            what = m.group('what')
            value = m.group('value')
            path = m.group('path')
            title = m.group('text')
            
            if what == 'legacy' and hasattr(self, 'lang'):
                key = '{}-{}'.format(self.lang, value)
                if key in self._context['uids']:
                    value = '/' + self._context['uids'][key].url
                    if not title:
                        title = self._context['uids'][key].title
                else:
                    value = '#legacy:' + value
                
            return '<a href="{}">{}<'.format(value, title)

        return hrefs.sub(replacer, content)

    def getLang(self):
        return "%s-%s" % (self.locale, getattr(self, 'global'))

class OvhEntityGenerator(EntityGenerator):
    class OvhSubEntityGenerator(EntityGenerator.EntitySubGenerator):
        def __init__(self, entity_type, *args, **kwargs):
            super(OvhEntityGenerator.OvhSubEntityGenerator, self) \
                .__init__(entity_type, *args, **kwargs)

        def add_legacy_id_path(self, content):
            if (not 'uids' in self.context):
                self.context.update({'uids': {}})

            if (content.metadata.get('legacy_guide_number')):
                legacy_guide_number = content.metadata.get('legacy_guide_number')
                key = '{}-{}'.format(content.lang, legacy_guide_number)
                key = key.replace('\'', '')
                self.context['uids'][key] = content

        def get_files(self, paths, exclude=[], extensions=None):
            files = []
            for path in paths:
                root = os.path.join(self.path, path) if path else self.path
                for filepath in glob.iglob(root, recursive=True):
                    files.append(filepath)

            return files
        
        def generate_context(self):
            """Add the entities into the shared context"""

            all_entities = []
            files = self.get_files(
                    self.settings['PATHS'],
                    exclude=self.settings['EXCLUDES'])

            for f in files:
                entity_or_draft = self.get_cached_data(f, None)
                if entity_or_draft is None:
                    entity_class = EntityFactory(
                        self.entity_type,
                        self.settings['MANDATORY_PROPERTIES'],
                        self.settings['DEFAULT_TEMPLATE'],
                        OvhEntity)
                    try:
                        entity_or_draft = self.readers.read_file(
                            base_path=self.path, path=f, content_class=entity_class,
                            context=self.context,
                            preread_signal=ovh_entity_subgenerator_preread,
                            preread_sender=self,
                            context_signal=ovh_entity_subgenerator_context,
                            context_sender=self)
                    except Exception as e:
                        logger.error('Could not process %s\n%s', f, e,
                            exc_info=self.settings.get('DEBUG', False))
                        self._add_failed_source_path(f)
                        continue

                    if not contents.is_valid_content(entity_or_draft, f):
                        self._add_failed_source_path(f)
                        continue

                    known_statuses = ("published", "draft")

                    if entity_or_draft.status.lower() not in known_statuses:
                        logger.warning("Unknown status '%s' for file %s, skipping it.",
                                       entity_or_draft.status, f)
                        self._add_failed_source_path(f)
                        continue

                    self.cache_data(f, entity_or_draft)

                if entity_or_draft.status.lower() == "published":
                    all_entities.append(entity_or_draft)

                self.add_legacy_id_path(entity_or_draft)
                self.add_source_path(entity_or_draft)

            self.entities, self.translations = process_translations(
                all_entities)

            sorter = self.settings["SORTER"]
            sorter(self.entities)

            # and generate the output :)

            # order the categories per name
            self.categories = []

            self.authors = []

            self.save_cache()
            self.readers.save_cache()

    def __init__(self, *args, **kwargs):
        super(OvhEntityGenerator, self).__init__(*args, **kwargs)