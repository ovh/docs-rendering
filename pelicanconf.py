#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import sys
sys.path.append('.')
from plugins.ovh_entities.ovh_entities import OvhEntityGenerator

AUTHOR = 'OVH'
SITENAME = "OVH Guides"
SITEURL = ''
TIMEZONE = "Europe/Paris"

PATH = "pages"
STATIC_PATHS = ['.']

THEME = "themes/ovh"

TRANSLATIONS_FILE = "config/translations.yml"

# can be useful in development, but set to False when you're ready to publish
RELATIVE_URLS = False

GITHUB_URL = "https://github.com/ovh/docs/blob/master/"
REVERSE_CATEGORY_ORDER = True
LOCALE = "C"
DEFAULT_PAGINATION = False
DEFAULT_DATE = (2012, 3, 2, 14, 1, 1)
DEFAULT_LANG = "fr-fr" 

PAGE_PATHS = []
ARTICLE_PATHS = []

LINKS = ()

# global metadata to all the contents
DEFAULT_METADATA = {'lang': 'fr-fr', 'locale': 'fr', 'global': 'fr', 'order': 'z', 'folder': '', 'summary': False,}

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    }

# code blocks with line numbers
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

# deactivation
PAGE_SAVE_AS = ''
PAGE_LANG_SAVE_AS = ''
ARTICLE_SAVE_AS = ''
ARTICLE_LANG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
STATIC_LANG_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAGS_SAVE_AS = ''

FEED_ATOM = None
FEED_ALL_ATOM = None
AUTHOR_FEED_ATOM = None
CATEGORY_FEED_ATOM = None
TAG_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
TRANSLATION_FEED_ALL_ATOM = None
TRANSLATION_AUTHOR_FEED_ATOM = None
TRANSLATION_CATEGORY_FEED_ATOM = None
TRANSLATION_TAG_FEED_ATOM = None

FEED_RSS = None
FEED_ALL_RSS = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_RSS = None
TAG_FEED_RSS = None
TRANSLATION_FEED_RSS = None
TRANSLATION_FEED_ALL_RSS = None
TRANSLATION_AUTHOR_FEED_RSS = None
TRANSLATION_CATEGORY_FEED_RSS = None
TRANSLATION_TAG_FEED_RSS = None

DIRECT_TEMPLATES = ['sitemap']
SITEMAP_SAVE_AS = 'sitemap.xml'

# plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['ovh_entities', 'ovh_filters', 'ovh_markdown']

MARKDOWN = {
    'extensions': ['markdown.extensions.codehilite', 'markdown.extensions.extra'],
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
    },
}

ZONES = {
    'en-au': 'Australia',
    'en-ca': 'Canada',
    'fr-ca': 'Québec',
    'cs-cz': 'Czech Republic',
    'de-de': 'Germany',
    'es-es': 'Spain',
    'fi-fi': 'Finland',
    'fr-fr': 'France',
    'en-gb': 'United Kingdom',
    'en-ie': 'Ireland',
    'it-it': 'Italy',
    'lt-lt': 'Lithuania',
    'nl-nl': 'Netherlands',
    'pl-pl': 'Poland',
    'pt-pt': 'Portugal',
    'fr-ma': 'Morocco',
    'mx': 'WorldSpanish',
    'fr-sn': 'Senegal',
    'fr-tn': 'Tunisia',
    'en-us': 'United States',
}

LANGS = {
    'en-au': 'English (Australia)',
    'en-ca': 'English (Canada)',
    'fr-ca': 'Français (Canada)',
    'cs-cz': 'Česky',
    'de-de': 'Deutsch',
    'es-es': 'Español',
    'fi-fi': 'Suomen kieli',
    'fr-fr': 'Français',
    'en-gb': 'English (GB)',
    'en-ie': 'English (Ireland)',
    'it-it': 'Italiano',
    'lt-lt': 'Lietuvių kalba',
    'nl-nl': 'Nederlands',
    'pl-pl': 'Polski',
    'pt-pt': 'Português',
    'en-us': 'English (US)',
}

ENTITY_TYPES = {
    "Home": {
        "PATHS": ["home.*.md"],
        "PATH_METADATA": r"home\.(?P<lang>(?P<locale>\w{2})-(?P<global>\w{2,4}))\.md",
        "SUBGENERATOR_CLASS": OvhEntityGenerator.OvhSubEntityGenerator,
        "CHILDREN": ["Universe"],
        "SKIP_SLUG": True,
        "IS_ROOT": True,
    },
    "Universe": {
        "PATHS": ["**/universe.*.md"],
        "PATH_METADATA": r"(?P<slug>([^\/]+\/)*(?P<folder>[^\/]+))\/universe\.(?P<lang>(?P<locale>\w{2})-(?P<global>\w{2,4}))\.md",
        "SUBGENERATOR_CLASS": OvhEntityGenerator.OvhSubEntityGenerator,
        "CHILDREN": ["Universe", "Product"],
        "EXCLUDE_SLUGS": ["Home"],
    },
    "Product": {
        "PATHS": ["**/product.*.md"],
        "PATH_METADATA": r"(?P<slug>([^\/]+\/)*(?P<folder>[^\/]+))\/product\.(?P<lang>(?P<locale>\w{2})-(?P<global>\w{2,4}))\.md",
        "SUBGENERATOR_CLASS": OvhEntityGenerator.OvhSubEntityGenerator,
        "CHILDREN": ["Guide"],
        "EXCLUDE_SLUGS": ["Home", "Universe"],
    },
    "Guide": {
        "PATHS": ["**/guide.*.md"],
        "PATH_METADATA": r"(?P<slug>([^\/]+\/)*(?P<folder>[^\/]+))\/guide\.(?P<lang>(?P<locale>\w{2})-(?P<global>\w{2,4}))\.md",
        "SUBGENERATOR_CLASS": OvhEntityGenerator.OvhSubEntityGenerator,
        "CHILDREN": ["Guide"],
        "EXCLUDE_SLUGS": ["Home", "Universe"],
    },
    "NotFound": {
        "PATHS": ["404.*.md"],
        "PATH_METADATA": r"(?P<slug>404)\.(?P<lang>(?P<locale>\w{2})-(?P<global>\w{2,4}))\.md",
        "SUBGENERATOR_CLASS": OvhEntityGenerator.OvhSubEntityGenerator,
        "CHILDREN": [],
        "IS_ROOT": True,
    },
}
