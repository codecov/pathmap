# -*- coding: utf-8 -*-

import os
import sys

from .tree import Tree

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
    # require N ancestors to be in common with original path and matched path
    pl = path.lower()
    ml = match.lower()
    if pl == ml:
        return True
    return ml.endswith('/'.join(pl.split('/')[(ancestors+1)*-1:]))


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

def _resolve_path(tree, path, ancestors=None):
    """
    Resolve a path

    :tree (Tree instance) Tree containing a lookup dictionary for paths
    :path (str) The path to be resolved
    :resolvers (list) Resolved changes

    returns new_path (str), pattern (list)
    """
    path = clean_path(path)

    new_path = tree.lookup(path)

    if new_path and ancestors and not _check_ancestors(path, new_path, ancestors):
        return None

    if new_path:
        return new_path

    # not found
    return None

def resolve_paths(toc, paths, ancestors=None):
    """
    :toc (str) e.g, ",real_path,another_real_path,"
    :paths (list) e.g. ["path", "another_path"]
    returns generated of resolved filepath names
    """
    tree = Tree()
    tree.construct_tree(toc)
    # keep a cache of known changes
    for path in paths:
        new_path = _resolve_path(tree, path,  ancestors)
        if new_path:
            # yield the match
            yield new_path
        else:
            yield None


def resolve_by_method(toc):
    """
    returns a method that can be called with a path to resolve
    """
    # keep a cache of known changes
    tree = Tree()
    tree.construct_tree(toc)

    def _resolve(path, ancestors=None):
        new_path = _resolve_path(tree, path, ancestors)
        if new_path:
            # yield the match
            return new_path
    return _resolve
