ifeq ($(OSTYPE),cygwin)
    CLEANUP=rm -f
    TARGET_EXTENSION=out
else ifeq ($(OS),Windows_NT)
    CLEANUP=del /F /Q
    TARGET_EXTENSION=exe
else
    CLEANUP=rm -f
    TARGET_EXTENSION=out
endif

PATHU = Unity/src/
PATHS = pathmap/
PATHT = tests/c/

SRCT = $(wildcard $(PATHT)*.c)
SRCS = $(wildcard $(PATHS)*.c)
SRCU = $(wildcard $(PATHU)*.c)

PYTHON_INCLUDES = $(shell python-config --includes)

C_COMPILER=gcc
ifeq ($(shell uname -s), Darwin)
C_COMPILER=clang
endif

CFLAGS = $(shell python-config --cflags)
CFLAGS += -I $(PATHU)

LDFLAGS = $(shell python-config --ldflags)

install:
	python setup.py install build_ext -i

testpy:
	py.test

testc:
	$(C_COMPILER) $(SRCT) $(SRCS) $(SRCU) $(CFLAGS) $(LDFLAGS) -o ctests.$(TARGET_EXTENSION) -v

clean:
	$(CLEANUP) *.$(TARGET_EXTENSION)


.PHONY: clean
.PHONY: test
