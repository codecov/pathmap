import pytest

from pathmap.tree import Tree


class TestTree(object):
    @classmethod 
    def setup_class(cls):
        cls.tree  = Tree()

    def setup_method(self, method):
        self.tree.instance = {}


    def test_tree_insert_new_path(self):
        path = 'a/b/c'
        self.tree.insert(path)

        assert(self.tree.instance == {
            'c': { 
                self.tree._ORIG: 'c',
                self.tree._END: False,
                'b' : { 
                    self.tree._ORIG: 'b',
                    self.tree._END: False,
                    'a' : {
                        self.tree._ORIG:'a',
                        self.tree._END: True
                    } 
                } 
            } 
        })

    def test_tree_insert_update(self):
        path = 'a/b/c'
        self.tree.insert(path)

        update = 'f/g/c'
        self.tree.insert(update)

        expected = {
            'c': {
                self.tree._ORIG: 'c',
                self.tree._END: False,
                'b' : {
                    self.tree._ORIG: 'b',
                    self.tree._END: False,
                    'a' : {
                        self.tree._ORIG: 'a',
                        self.tree._END: True
                    }
                },
                'g' : {
                    self.tree._ORIG: 'g',
                    self.tree._END: False,
                    'f' : {
                        self.tree._ORIG: 'f',
                        self.tree._END: True
                    }
                },
            }
        }

        assert(self.tree.instance == expected)

    def test_constructing_tree(self):
        toc = 'b/c,A/b/c'
        self.tree.construct_tree(toc)
        expected = {
            'c' : {
                self.tree._ORIG: 'c',
                self.tree._END: False,
                'b' : {
                    self.tree._ORIG: 'b',
                    self.tree._END: True,
                    'a' : {
                        self.tree._ORIG: 'A',
                        self.tree._END: True
                    }
                }
            }
        }

        assert(self.tree.instance == expected)

    def test_recursive_lookup(self):
        d = {
            'c.py': { 
                self.tree._ORIG : 'C.py', 
                self.tree._END: False,
                'b' : {
                    self.tree._ORIG: 'B',
                    self.tree._END: True
                }
            }
        }

        path_parts = ['C.py','b']

        results = []
        self.tree._recursive_lookup(d, path_parts, results)

        assert(results == ['C.py','B'])

    def test_lookup(self):
        toc = 'a/b/c,b/C.py'
        search = 'b/c.py'

        self.tree.construct_tree(toc)
        path = self.tree.lookup(search)

        assert(path == 'b/C.py')
