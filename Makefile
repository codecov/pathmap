test:
	py.test -v

benchmarks:
	python tests/benchmarks.py

profile:
	python -m memory_profiler tests/profile.py
