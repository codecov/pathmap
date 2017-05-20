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
    slash_pattern,
    extract_match,
    resolve_path, 
    resolve_path_if_long, 
    resolve_path_if_short, 
    resolve_paths
)

from lcs import longest_common_substring

# ========== Mock data ===========
before = [
    'very/long/path.py',
    'before/path.py',
    'not/found.py',
    '/Users/user/owner/repo/dist/components/login.js',
    'site-packages/package/__init__.py',
    'path.py'
]

after = [
    'long/path.py',
    'after/path.py',
    None,
    'src/components/login.js',
    'package/__init__.py',
    'path.py'
]

toc = ','.join(map(lambda x: "" if x == None else x, after))

# ========= END Mock data ==========
def test_clean_path():
    path = '**/some/directory'
    assert clean_path(path) == 'some/directory'
    path = 'some/path\r/with/tabs\r'
    assert clean_path(path) == 'some/path/with/tabs'
    path = 'some\ very_long/directory\ name'
    assert clean_path(path) == 'some very_long/directory name'
    path = 'ms\\style\\directory'
    assert clean_path(path) == 'ms/style/directory'

def test_slash_pattern():
    has_slash = 'slash/'
    assert slash_pattern(has_slash) == 'slash/'

def test_extract_match():
    index = toc.find('components')
    extracted = extract_match(toc, index)
    assert extracted == 'src/components/login.js'

def test_longest_common_substring():
    paths = ','.join(before)
    result = longest_common_substring('some/folder/../repo/dist/components/login.js', paths)
    assert result == '/repo/dist/components/login.js'

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
