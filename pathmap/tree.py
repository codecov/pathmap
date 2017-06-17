from .utils import _extract_match
import collections

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

        extra data:

            _end_ - Marks the end of the list
            E.g.:
                ['a','b'] => { 'b' : { 'a' : {}, '_end_': True}, '_end_': False}

            _orig_ - The original value of the key/list item
            E.g.:
                ['A'] => { 'a' : {}, '_orig_': 'A', '_end_': True}
        """
        d = {}
        for i in range(0, len(lis)):
            d[self._END] = True if i == 0 else False
            d[self._ORIG] = lis[i]
            d = {lis[i].lower(): d}
        return d

    def _recursive_lookup(self, d, lis, results, i = 0, end=False):
        """
        Performs a lookup in tree recursively

        :dict: d - tree branch
        :list: lis - list of strings to search for
        :list: results - Collected hit results
        :int: i - Index of lis
        :bool: end - Indicates if last lookup was the end of a sequence

        :returns a list of hit results
        """
        key = None

        if i < len(lis):
            key = lis[i].lower()
        
        if d.get(key):
            results.append(d.get(key).get(self._ORIG))
            root = d.get(key)
            return self._recursive_lookup(
                root, 
                lis,
                results,
                i + 1,
                root.get(self._END)
            )
        else:
            if not end:
                results = []
            return results

    def lookup(self, path):
        """
        Lookup a path in the tree

        :str: path - The path to search for

        :returns The closest matching path in the tree if present else None
        """
        path_split = list(reversed(path.split('/')))
        results = self._recursive_lookup(self.instance, path_split, [])

        if not results:
            return None

        path_hit = '/'.join(reversed(results))

        return path_hit

    def _update(self, d, u):
        """
        Update a dictionary
        :dict: d - Dictionary being updated
        :dict: u - Dictionary being merged
        """
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                r = self._update(d.get(k, {}), v)
                d[k] = r
            else:
                if k == self._END  and d.get(k) == True:
                    pass
                else:
                    d[k] = u[k]
        return d


    def insert(self, path):
        """
        Insert a path into the tree

        :str: path - The path to insert
        """

        path_split = path.split('/')
        root_key =  path_split[-1]
        root = self.instance.get(root_key)

        if not root:
            u = self._list_to_nested_dict(path_split)
            self.instance.update(u)
        else:
            u = self._list_to_nested_dict(path_split[:-1])
            self.instance[root_key] = self._update(root, u)

    def construct_tree(self, toc):
        """
        Constructs a tree

        :str: toc - The table of contents
        """
        constructing = True
        toc_index    = 1

        while constructing:
            if toc_index < len(toc) - 1:
                path = _extract_match(toc, toc_index)
                if path:
                    self.insert(path)
                    toc_index = toc_index  + len(path) + 2
                else:
                    if toc[toc_index] == ',':
                        toc_index += 1
            else:
                constructing = False
                break
