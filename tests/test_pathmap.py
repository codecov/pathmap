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
    "before/path.py",
    "not/found.py",
    "/Users/user/owner/repo/dist/components/login.js",
    "site-packages/package/__init__.py"
]

after = [
    "after/path.py",
    None,
    "src/components/login.js",
    "package/__init__.py"
]

toc = ",".join([
    "",
    "after/path.py",
    "src/components/login.js",
    "package/__init__.py"
    "__init__.py",
    "setup.py"
])
# ========= END Mock data ==========


def test_resolve_path_if_long():
    path = '/Users/user/owner/repo/dist/components/login.js'
    (new_path, pattern) = resolve_path_if_long(toc, path)
    assert new_path == 'src/components/login.js'
    assert pattern == ('/Users/user/owner/repo/dist','src')

