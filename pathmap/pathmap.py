# -*- coding: utf-8 -*-

import os

import sys

from lcs import longest_common_substring
from operator import itemgetter


relpath = os.path.relpath


def clean_path(path):
    path = relpath(
        path.strip()
            .replace('**/', '')
            .replace('\r', '')
            .replace('\\ ', ' ')
            .replace('\\', '/')
    )
    return path

def _check_ancestors(path, match, ancestors):
    anc = ancestors + 1
    split_path = path.lower().split('/')
    split_match = match.lower().split('/')

    if len(split_path) < anc or len(split_match) < anc:
        return False

    path_ancestors  = split_path[len(split_path) - anc:]
    match_ancestors = split_match[len(split_match) - anc:]

    return path_ancestors == match_ancestors

def _slash_pattern(pattern):
    """
    Checks if pattern ends with a slash and appends one if slash is not present

    :pattern (str) pattern added/removed

    returns a pattern with slash
    """
    if pattern.endswith('/'):
        return pattern
    else:
        return '%s/' % pattern


def _extract_match(toc, index):
    """
    Extracts a path between seperators (,)

    :toc (str) Table of contents
    :index (int) Index of match

    returns full path from match
    """
    length = len(toc)
    start_index = index
    while toc[start_index] != ',' and start_index >= 0:
        start_index -= 1
    end_index = index
    while toc[end_index] != ',' and end_index < length - 1:
        end_index += 1
    return toc[start_index+1:end_index]


def _resolve_path(toc, path, resolvers, ancestors=None):
    """
    Resolve a path

    :toc (str) Table of contents
    :path (str) The path to be resolved
    :resolvers (list) Resolved changes

    returns new_path (str), pattern (list)
    """
    path = clean_path(path)

    _pattern = ',{}{},'.format
    # direct match
    if _pattern(path, '') in toc:
        return path, None

    # known changes
    _path_startswith = path.startswith
    for (remove, add) in resolvers:
        if _path_startswith(remove):
            _path = _pattern(add, path[len(remove):])
            if _path in toc:
                return _path[1:-1], None

    # path may be to long
    (new_path, pattern) = _resolve_path_if_long(toc, path, ancestors)
    if new_path:
        return new_path, pattern

    # not found
    return None, None


def _resolve_path_if_long(toc, path, ancestors=None):
    """
    Resolves a long path, e.g.: very/long/path.py => long/path.py

    :toc (str) Table of contents
    :path (str) Path to resolve

    returns new_path (str), pattern (list)
    """
    # maybe regexp style resolving and take the longest discovered pathname

    # Find the longest common substring
    loc = longest_common_substring(path, toc)

    if loc:
        # Find the index that matches the loc
        index = toc.lower().find(loc.lower())
        # Extract string from location
        # and remove extra ',' characters if present
        match = _extract_match(toc, index).replace(',','')

        # If ancestors are declared check if they are valid
        if ancestors:
            if not _check_ancestors(path, match, ancestors):
                return None, None

        # We expect the longest common substring
        # to have a match in the end of the string
        if not match.lower().endswith(loc.lower()):
            return None, None

        # If we have a match in the end we make sure
        # that this is a full match of the filename and
        # not partial match
        if path.lower().split('/')[-1] != match.lower().split('/')[-1]:
            return None, None

        # Remove pattern
        rm_pattern = path.replace(loc, '')
        if rm_pattern:
            rm_pattern = _slash_pattern(rm_pattern)
        # Add pattern
        add_pattern = match.replace(loc, '')
        if add_pattern:
            add_pattern = _slash_pattern(add_pattern)
        return match, (rm_pattern, add_pattern)
    else:
        return None, None


def resolve_paths(toc, paths, ancestors=None):
    """
    :toc (str) e.g, ",real_path,another_real_path,"
    :paths (list) e.g. ["path", "another_path"]
    returns generated of resolved filepath names
    """
    # keep a cache of known changes
    resolvers = []
    for path in paths:
        (new_path, resolve) = _resolve_path(toc, path, resolvers, ancestors)
        if new_path:
            # yield the match
            yield new_path
            # add known resolve
            if resolve:
                resolvers.append(resolve)
        else:
            yield None


def resolve_by_method(toc):
    """
    returns a method that can be called with a path to resolve
    """
    # keep a cache of known changes
    resolvers = []

    def _resolve(path, ancestors=None):
        (new_path, resolve) = _resolve_path(toc, path, resolvers, ancestors)
        if new_path:
            # add known resolve
            if resolve:
                resolvers.append(resolve)
            # yield the match
            return new_path

    return _resolve
