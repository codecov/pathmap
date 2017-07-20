import collections
import operator

from .utils import _extract_match
from difflib import SequenceMatcher


class Tree:
    def __init__(self, *args, **kwargs):
        self.instance = {}

        # Sequence end indicator
        self._END = '\\*__ends__*//'

        # Original value indicator
        self._ORIG = '\\*__orig__*//'

    def _list_to_nested_dict(self, lis):
        """
        Turns a list into a nested dict

        E.g.:
            ['a','b','c'] => { 'c' : { 'b' : { 'a' : {} } } }
        """
        d = {}
        for i in range(0, len(lis)):
            d[self._END] = True if i == 0 else False
            d[self._ORIG] = ['/'.join(lis[i:])]
            d = {lis[i].lower(): d}
        return d

    def _get_best_match(self, path, possibilities):
        """
        Given a path find how similar it is to all paths in possibilities

        :str: path - A path part E.g.: a/b.py => a
        :list: possibilities - Collected possibilities
        """

        # Map out similarity of possible paths with the path being looked up
        similarity = list(map(lambda x: SequenceMatcher(None, path, x).ratio(), possibilities))

        # Get the index, value of the most similar path
        index, value = max(enumerate(similarity), key=operator.itemgetter(1))

        return possibilities[index]

    def _drill(self, d, results):
        """
        Drill down a branch of a tree.
        Collects results until a ._END is reached.

        :returns - A list containing a possible path or None
        """
        if not d or d.get(self._ORIG) and len(d.get(self._ORIG)) > 1:
            return None

        root = d.get(list(d.keys())[0])

        if root.get(self._END):
            return root.get(self._ORIG)
        else:
            return self._drill(root, results)

    def _recursive_lookup(self, d, lis, results, i=0, end=False):
        """
        Performs a lookup in tree recursively

        :dict: d - tree branch
        :list: lis - list of strings to search for
        :list: results - Collected hit results
        :int: i - Index of lis
        :bool: end - Indicates if last lookup was the end of a sequence

        :returns a list of hit results if path is found in the tree
        """
        key = None

        if i < len(lis):
            key = lis[i].lower()

        root = d.get(key)
        if root:
            results = root.get(self._ORIG)
            return self._recursive_lookup(
                root,
                lis,
                results,
                i + 1,
                root.get(self._END)
            )
        else:
            if not end and results:
                results = []
                next_path = self._drill(d, results)
                if next_path:
                    results.extend(next_path)
            return results

    def lookup(self, path):
        """
        Lookup a path in the tree

        :str: path - The path to search for
    
        :returns The closest matching path in the tree if present else None
        """
        path_hit = None
        path_split = list(reversed(path.split('/')))
        results = self._recursive_lookup(self.instance, path_split, [])

        if not results:
            return None

        if len(results) == 1:
            path_hit = results[0]
        else:
            path_hit = self._get_best_match(path, list(reversed(results)))

        return path_hit

    def update(self, d, u):
        """
        Update a dictionary
        :dict: d - Dictionary being updated
        :dict: u - Dictionary being merged
        """
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                r = self.update(d.get(k, {}), v)
                d[k] = r
            else:
                if k == self._END and d.get(k) is True:
                    pass
                elif k == self._ORIG and d.get(k) and u.get(k):
                    if d[k] != u[k]:
                        d[k] = d[k] + u[k]
                else:
                    d[k] = u[k]
        return d

    def insert(self, path):
        """
        Insert a path into the tree

        :str: path - The path to insert
        """

        path_split = path.split('/')
        root_key = path_split[-1].lower()
        root = self.instance.get(root_key)

        if not root:
            u = self._list_to_nested_dict(path_split)
            self.instance.update(u)
        else:
            u = self._list_to_nested_dict(path_split)
            self.instance = self.update(self.instance, u)

    def construct_tree(self, toc):
        """
        Constructs a tree

        :str: toc - The table of contents
        """
        constructing = True
        toc_index = 1

        while constructing:
            if toc_index < len(toc) - 1:
                path = _extract_match(toc, toc_index)
                if path:
                    self.insert(path)
                    toc_index = toc_index + len(path) + 1
                else:
                    if toc[toc_index] == ',':
                        toc_index += 1
            else:
                constructing = False
                break
