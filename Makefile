test:
	clang tests/c/test_lcs.c pathmap/lcsmodule.c Unity/src/unity.c -o test_pathmap -Wno-unused-result -Wsign-compare -Wunreachable-code -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/Users/Donna/.pyenv/versions/3.6.0/include/python3.6m 
clean:
	rm test_pathmap
