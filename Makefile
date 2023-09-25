repro: cython_module
	command time python repro.py 10
	command time python repro.py 20

test: cython_module
	python -m pytest test.py

inspect: cython_module
	python inspect_leak.py

cython_module:
	CPPFLAGS='-DCYTHON_FAST_THREAD_STATE=1' cythonize -X language_level=3 -f -i lib.pyx

clean:
	rm -rf lib.c *.so build/

.PHONY: repro test inspect cython_module clean
