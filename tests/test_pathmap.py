#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_revolver
----------------------------------

Tests for `pathmap` module.
"""

import pytest

from pathmap import (
    clean_path, 
    resolve_path, 
    resolve_path_if_long, 
    resolve_path_if_short, 
    resolve_path_if_obscure,
    resolve_paths
)

# ========== Mock data ===========
before = [
    "very/long/path.py",
    "before/path.py",
    "not/found.py",
    "/Users/user/owner/repo/dist/components/login.js",
    "site-packages/package/__init__.py",
    "path.py"
]

after = [
    "long/path.py",
    "after/path.py",
    None,
    "src/components/login.js",
    "package/__init__.py",
    "path.py"
]

toc = ','.join(map(lambda x: "" if x == None else x, after))

# ========= END Mock data ==========

def test_resolve_path_if_long():
    path = '/Users/user/owner/repo/dist/components/login.js'
    (new_path, pattern) = resolve_path_if_long(toc, path)
    assert new_path == 'src/components/login.js'
    assert pattern == ('/Users/user/owner/repo/dist/','src/')

def test_resolve_path():
    # short to long
    path = 'components/login.js'
    (new_path, pattern) = resolve_path(toc, path, [])
    assert new_path == 'src/components/login.js'
    assert pattern  == ('', 'src/')


def test_resolve_paths():
    resolved_paths = resolve_paths(toc, before)
    assert set([r for r in resolved_paths]) == set(after)
