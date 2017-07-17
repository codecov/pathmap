import pytest

from pathmap.tree import Tree


class TestTree(object):
    @classmethod 
    def setup_class(cls):
        cls.tree  = Tree()

    def setup_method(self, method):
        self.tree.instance = {}

    def test_drill(self):
        """
        Test drilling a branch of tree
        """
        results = []
        nested = self.tree._list_to_nested_dict(['a','b','c'])
        assert self.tree._drill(nested, []) == ['a/b/c']
