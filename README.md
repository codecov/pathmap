Pathmap
========

[![Build Status](https://travis-ci.org/codecov/pathmap.svg?branch=master)](https://travis-ci.org/codecov/pathmap)

[![codecov](https://codecov.io/gh/codecov/pathmap/branch/master/graph/badge.svg)](https://codecov.io/gh/codecov/pathmap)

### Installation

	make install

### Testing

To run python tests

	make test

To run C tests you will need to clone the Unity C test framework to the repository root.
It is ignored by default.

	git clone https://github.com/ThrowTheSwitch/Unity

Then run C tests with

	make testc
