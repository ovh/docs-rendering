import unittest
from jinja2 import Environment, BaseLoader
from entities import Entity

import sys
sys.path.append('../..')
from ovh_filters.tree import tree


class CustomEntity(Entity):
    @property
    def url(self):
        return self.custom_url


class TestTree(unittest.TestCase):

    def mockEntity(self, title, children=None, url=None, parent=None, type=None):
        entity = CustomEntity(content=None)
        entity.title = title
        entity.children = children
        entity.custom_url = url
        entity.parent = parent
        entity.type = type
        return entity

    def test_tree_entity_with_children(self):
        baseEntity = self.mockEntity('Parent')

        child1 = self.mockEntity('Child1', url='/a/test')
        child2 = self.mockEntity('Child2', url='/b/test2')

        baseEntity.children = [
            child1,
            child2
        ]

        result = tree(baseEntity)
        expected = {
            'title': baseEntity.title,
            'url': baseEntity.url,
            'active': True,
            'children': [
                {
                    'title': child1.title,
                    'active': False,
                    'url': child1.url,
                },
                {
                    'title': child2.title,
                    'active': False,
                    'url': child2.url,
                },
            ]
        }

        self.assertEqual(result, expected)

    def test_tree_child_guide(self):
        baseEntity = self.mockEntity(title="Parent", type="Guide")
        child1 = self.mockEntity(title="Child1", type="Guide", parent=baseEntity)
        child2 = self.mockEntity(title="Child2", type="Guide", parent=baseEntity)
        baseEntity.children = [
            child1,
            child2
        ]

        result = tree(child1)
        expected = {
            'title': baseEntity.title,
            'active': False,
            'url': baseEntity.url,
            'children': [
                {
                    'title': child1.title,
                    'active': True,
                    'url': child1.url,
                },
                {
                    'title': child2.title,
                    'active': False,
                    'url': child2.url,
                },
            ]
        }

        self.assertEqual(result, expected)

    def test_tree_entity_with_children_2_levels_deep(self):
        baseEntity = self.mockEntity(title="Parent", type="Guide")
        child1 = self.mockEntity(title="Child1", type="Guide", parent=baseEntity)
        child2 = self.mockEntity(title="Child2", type="Guide", parent=child1)
        child3 = self.mockEntity(title="Child3", type="Guide", parent=child2)
        child4 = self.mockEntity(title="Child4", type="Guide", parent=child1)

        child2.children = [ child3 ]
        child1.children = [ child2, child4 ]
        baseEntity.children = [ child1 ]

        result = tree(child3)
        expected = {
            'title': baseEntity.title,
            'url': baseEntity.url,
            'active': False,
            'children': [
                {
                    'title': child1.title,
                    'active': False,
                    'url': child1.url,
                    'children': [
                        {
                            'title': child2.title,
                            'url': child2.url,
                            'active': False,
                            'children': [
                                {
                                    'title': child3.title,
                                    'active': True,
                                    'url': child3.url,
                                }
                            ]
                        },
                        {
                            'title': child4.title,
                            'active': False,
                            'url': child4.url,
                        },
                    ]
                    },
                ]
            }

        self.assertEqual(result, expected)

