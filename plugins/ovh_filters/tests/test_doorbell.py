#!/usr/bin/env python
import unittest
from jinja2 import Environment, BaseLoader
from entities import Entity

import sys
sys.path.append('../..')
from ovh_filters.doorbell import doorbell

DOORBELL_API = {
    'en': {
        'id': 'doorbell_id_en',
        'key': 'doorbell_key_en',
    },
    'de': {
        'id': 'doorbell_id_de',
        'key': 'doorbell_key_de',
    },
    'fr': {
        'id': 'doorbell_id_fr',
        'key': 'doorbell_key_fr',
    },
    'es': {
        'id': 'doorbell_id_es',
        'key': 'doorbell_key_es',
    },
    'it': {
        'id': 'doorbell_id_it',
        'key': 'doorbell_key_it',
    },
    'pl': {
        'id': 'doorbell_id_pl',
        'key': 'doorbell_key_pl',
    },
    'pt': {
        'id': 'doorbell_id_pt',
        'key': 'doorbell_key_pt',
    },
}

class TestDoorbell(unittest.TestCase):

    def mockEntity(self, locale):
        """Mock an entity

        Args:
            locale (string): a locale string e.g: en, fr, ...

        Returns:
            A dict representing an entity
        """
        entity = Entity(content=None)
        entity.locale = locale
        return entity

    def generateEnvironment(self):
        """Generate the jinja2 environment with the filter to test

        Returns:
            The jinja2 environment
        """
        env = Environment(
            loader=BaseLoader()
        )

        env.filters['doorbell'] = doorbell

        return env

    def renderString(self, content="", ctx={}, env=None):
        """Render a string using jinja2

        Args:
            content (string): the string to render
            ctx (dict): the rendering context
            env (jinja2.Environment): a specific jinja2 environment

        Returns:
            the rendered content
        """
        if not env:
            env = Environment(loader=BaseLoader())

        return env.from_string(content).render(ctx)

    def getContent(self):
        return """
            {% set doorbell = entity|doorbell %}
            {{ doorbell.id }}
            {{ doorbell.key }}
        """

    def getExpected(self, locale):
        return """
            {}
            {}
        """.format(
            DOORBELL_API.get(locale).get('id'),
            DOORBELL_API.get(locale).get('key'),
        )

    def test_doorbell(self):
        """Test doorbell filter
        """

        locale = 'fr'
        content = self.getContent()
        result = self.getExpected(locale)

        context = {
            'entity': self.mockEntity(locale),
            'DOORBELL_API': DOORBELL_API,
        }

        rendered = self.renderString(content,
                                    context,
                                    self.generateEnvironment())

        self.assertEqual(rendered.strip(), result.strip())

    def test_doorbell_unknown_locale(self):
        """Test doorbell filter with an unknown locale
        """

        locale = 'unknown'
        content = self.getContent()
        result = ''
        context = {
            'entity': self.mockEntity(locale),
            'DOORBELL_API': DOORBELL_API,
        }

        rendered = self.renderString(content,
                                    context,
                                    self.generateEnvironment())

        self.assertEqual(rendered.strip(), result.strip())

    def test_doorbell_unset_locale(self):
        """Test doorbell filter with an entity without locale
        """

        # Test with no locale defined
        content = self.getContent()
        result = self.getExpected('en')
        context = {
            'entity': Entity(content=None),
            'DOORBELL_API': DOORBELL_API,
        }

        rendered = self.renderString(content,
                                    context,
                                    self.generateEnvironment())

        self.assertEqual(rendered.strip(), result.strip())

        # Test with locale as None
        context['entity'].locale = None
        rendered = self.renderString(content,
                                    context,
                                    self.generateEnvironment())

        self.assertEqual(rendered.strip(), result.strip())


if __name__ == '__main__':
    unittest.main()
