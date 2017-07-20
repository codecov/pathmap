Pathmap
========

[![Build Status](https://travis-ci.org/codecov/pathmap.svg?branch=master)](https://travis-ci.org/codecov/pathmap)

[![codecov](https://codecov.io/gh/codecov/pathmap/branch/master/graph/badge.svg)](https://codecov.io/gh/codecov/pathmap)

Pathmap is a library for resolving paths. Example

```
>>> from pathmap import resolve_paths
>>> toc = ',a/b/c,'
>>> paths = ['b/c']
>>> list(resolve_paths(toc, paths))

['a/b/c']

```

### Case sensitivity

Pathmap searches for paths using lower case keys only but it stores the original value 
of each path added to the tree. This way we can search for two identical paths with
different casing

```
>>> from pathmap import resolve_paths
>>> toc = ',a/b/C,A/B/c,'
>>> paths = ['A/b/C','a/B/c']
>>> list(resolve_paths(toc, paths))

['a/b/C', 'A/B/c']

```

### Resolving shorter/longer paths

When resolving paths it may happen that we get a partial path. For example searching for the path "two/three.py" in a tree that contains the path "dist/one/two/three.py".
Pathmap will continue searhing for a possible match until it hits the end of the current sequence but only if there is a single possible result.

For example if we add to our example 

```

toc = '''
dist/one/two/three.py
dist/another/two/three.py
'''

```

With this toc we would construct a tree that looks something like this

```
    three.py
        |
       two
    |       |
   one    another
    |       |
   dist   dist
```

Now when we hit the branch containing the key "two" we have two possible options, either
we resolve the path to "dist/one/two/three.py" or "dist/another/two/three.py". 
In this case pathmap will not resolve the path and simply return None.

### Local development

Dependencies are listed in the requirements_dev.txt file

	pip install -r requirements_dev.txt
	
### Testing

pytest is used for testing. Run tests with

	py.test

