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
    _slash_pattern,
    _extract_match,
    _resolve_path,
    _resolve_path_if_long,
    _check_ancestors,
    resolve_paths,
    resolve_by_method
)

from lcs import longest_common_substring


# ========== Mock data ===========
before = [
    'before/path.py',
    'before/path.py',
    'not/found.py',
    '/Users/user/owner/repo/dist/components/login.js',
    'site-packages/package/__init__.py',
    'path.py',
    'a/b/../Path With\\ Space'
]

after = [
    'after/path.py',
    'after/path.py',
    None,
    'src/components/login.js',
    'package/__init__.py',
    'path.py',
    'a/Path With Space'
]

toc = ','.join(map(lambda x: "" if x is None else x, after)) + ','


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
    assert _slash_pattern(has_slash) == 'slash/'


def test_extract_match():
    toc = ',src/components/login.js,'
    index = toc.find('components')
    extracted = _extract_match(toc, index)
    assert extracted == 'src/components/login.js'


def test_longest_common_substring():
    paths = ','.join(before)
    result = longest_common_substring('some/folder/../repo/dist/components/login.js', paths)
    assert result == '/repo/dist/components/login.js'


def test_resolve_path_if_long():
    path = '/Users/user/owner/repo/dist/components/login.js'
    (new_path, pattern) = _resolve_path_if_long(toc, path)
    assert new_path == 'src/components/login.js'
    assert pattern == ('/Users/user/owner/repo/dist/', 'src/')


def test_resolve_path_if_long_empty():
    (new_path, pattern) = _resolve_path_if_long('', '')
    assert (new_path, pattern) == (None, None)
    (new_path, pattern) = _resolve_path_if_long('abc/xyz', 'abc')
    assert (new_path, pattern) == (None, None)


def test_resolve_path():
    # short to long
    path = 'components/login.js'
    (new_path, pattern) = _resolve_path(toc, path, [])
    assert new_path == 'src/components/login.js'
    assert pattern == ('', 'src/')


def test_resolve_paths():
    resolved_paths = resolve_paths(toc, before)
    first = set([r for r in resolved_paths])
    second = set(after)
    assert first == second


def test_resolve_by_method():
    resolver = resolve_by_method(toc)
    assert callable(resolver)
    first = set(map(resolver, before))
    second = set(after)
    assert first == second


def test_check_ancestors():
    ancestors = 1
    path = 'one/two/three'
    match = 'four/two/three'

    assert _check_ancestors(path, match, ancestors) is True
    match = 'four/five/three'
    assert _check_ancestors(path, match, ancestors) is False


def test_resolve_paths_with_ancestors():
    toc = ',x/y/z,'

    # default, no ancestors ============================
    paths = ['z', 'R/z', 'R/y/z', 'x/y/z', 'w/x/y/z']
    expected = ['x/y/z', 'x/y/z', 'x/y/z', 'x/y/z', 'x/y/z']
    resolved = list(resolve_paths(toc, paths))

    assert set(resolved) == set(expected)
    # one ancestors ====================================
    paths = ['z', 'R/z', 'R/y/z', 'x/y/z', 'w/x/y/z']
    expected = [None, None, 'x/y/z', 'x/y/z', 'x/y/z']
    resolved = list(resolve_paths(toc, paths, 1))

    assert set(resolved) == set(expected)

    # two ancestors ====================================
    paths = ['z', 'R/z', 'R/y/z', 'x/y/z', 'w/x/y/z']
    expected = [None, None, None,  'x/y/z', 'x/y/z']
    resolved = list(resolve_paths(toc, paths, 2))

    assert set(resolved) == set(expected)


def test_case_sensitive_ancestors():
    toc = ',src/HeapDump/GCHeapDump.cs,'
    path = 'C:/projects/perfview/src/heapDump/GCHeapDump.cs'
    (path, pattern) = _resolve_path_if_long(toc, path, 1)

    assert path == 'src/HeapDump/GCHeapDump.cs'


def test_path_should_not_resolve():
    resolvers = []
    toc = ',four/six/three.py,'
    path = 'four/six/seven.py'
    (path, pattern) = _resolve_path(toc, path, resolvers)

    assert path is None
    assert pattern is None
