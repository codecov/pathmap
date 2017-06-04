from .utils import _extract_match
from lcs import longest_common_substring

class Tree:
    def __init__(self, *args, **kwargs):
        self.cache = {}
        self.tree  = {}
        self.paths = None

    def find_all(self, a_str, sub):
        """
        Find all instances of substring within string

        a_str (str) The string to search in
        sub (str) The string to look for
        """
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches

    def lookup(self, path):
        """
        Lookup key=path within tree
        """
        return self.tree.get(path)

    def find_path(self, path):
        """
        Find path based on the longest common substring 
        between path/lookup results

        Returns a tuple of 
            longest_common_substring
            extracted match from self.paths
        """

        if not path:
            return None, None

        filename = path.split('/')[-1].lower()
        hit      = self.lookup(filename)
        if not hit:
            return None, None
        longest = longest_common_substring(path, hit)
        match_index = hit.lower().find(longest.lower())
        return (longest, _extract_match(hit, match_index))

    def construct_tree(self, paths):
        """
        Constructs a lookup tree from paths

        :paths (str) A comma seperated string of paths

        returns A tree instance
        """
        self.paths = paths
        paths_lis = paths.split(',')
        for p in paths_lis:
            filename = p.split('/')[-1].lower()

            # Check if filename has been handled
            if self.lookup(filename) or len(filename) == 0:
                pass
            else:
                # Find all instances where this particular
                # filename occurs in paths
                file_indexes = list(self.find_all(paths.lower(), filename))
                files = list(map(lambda x: _extract_match(paths, x), file_indexes))
                if files:
                    self.tree[filename] = ','.join(files)
        return self.tree
