# -*- coding: utf-8 -*-

import os

relpath = os.path.relpath

def longest_common_substring(s1, s2):
    """
    Finds the longest common substring for s1 in s2
    """
   m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
   longest, x_longest = 0, 0
   for x in range(1, 1 + len(s1)):
       for y in range(1, 1 + len(s2)):
           if s1[x - 1] == s2[y - 1]:
               m[x][y] = m[x - 1][y - 1] + 1
               if m[x][y] > longest:
                   longest = m[x][y]
                   x_longest = x
           else:
               m[x][y] = 0
   return s1[x_longest - longest: x_longest]

def clean_path(path):
    path = relpath(path.strip()
                   .replace('**/','')
                   .replace('\r', '')
                   .replace('\\ ', ' ')
                   .replace('\\', '/'))
    return path

def slash_pattern(pattern):
    """
    Checks if pattern ends with a slash and appends one if slash is not present
    """
    return pattern if pattern.endswith('/') else '%s/' % pattern

def extract_match(toc, index):
    length = len(toc)
    start_index = index
    while toc[start_index] != ',' and start_index >= 0:
        start_index -= 1
    end_index = index
    while toc[end_index] != ',' and end_index < length - 1:
        end_index += 1
    if end_index == length - 1:
        end_index += 1
    return toc[start_index+1:end_index]


def resolve_path(toc, path, resolvers):
    # direct match
    if ',{},'.format(path) in toc:
        return path, None

    # known changes
    for (remove, add) in resolvers:
        if path.startswith(remove):
            _path = ',{}{},'.format(add, path.replace(remove, ''))
            if _path in toc:
                return _path[1:-1], None

    # path may be to long
    (new_path, pattern) = resolve_path_if_long(toc, path)
    if new_path:
        return new_path, pattern

    (new_path, pattern) = resolve_path_if_short(toc, path)
    if new_path:
        return new_path, pattern

    (new_path, pattern) = resolve_path_if_obscure(toc, path)
    if new_path:
        return new_path, pattern

    # not found
    return None, None


def resolve_path_if_long(toc, path):
    """
    Resolves a long path, e.g.: very/long/path.py => long/path.py
    """
    # maybe regexp style resolving and take the longest discovered pathname

    # Find the longest common substring 
    loc = longest_common_substring(path, toc)
    if loc:
        # Find the index that matches the loc
        index = toc.find(loc)
        # Extract string from location
        match = extract_match(toc, index)
        # Remove pattern
        rm_pattern  = path.replace(loc, '')
        if rm_pattern:
            rm_pattern = slash_pattern(rm_pattern)
        # Add pattern
        add_pattern = match.replace(loc, '')
        if add_pattern:
            add_pattern = slash_pattern(add_pattern)
        return match, (rm_pattern, add_pattern)
    else:
        return None, None

def resolve_path_if_short(toc, path):
    # Doddies short path fix concept
    index = toc.find(path)
    if index != -1:
        match = extract_match(toc,index)
        pattern = match.replace(path, '')
        return extract_match(toc, index), ('', pattern)
    else:
        return None, None

def resolve_path_if_obscure(toc, path):
    # maybe regexp style resolving and take the longest discovered pathname
    return None, None


def resolve_paths(toc, paths):
    """
    :toc (str) e.g, ",real_path,another_real_path,"
    :paths (list) e.g. ["path", "another_path"]
    returns generated of resolved filepath names
    """
    # keep a cache of known changes
    resolvers = []
    for path in paths:
        (new_path, resolve) = resolve_path(toc, path, resolvers)
        if new_path:
            # Remove the path from toc
            toc = toc.replace(new_path, '')
            # yield the match
            yield new_path
            # add known resolve
            if resolve:
                resolvers.append(resolve)
        else:
            yield None
