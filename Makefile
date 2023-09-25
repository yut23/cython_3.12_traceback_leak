test: cython_module
	command time python test.py 10
	command time python test.py 20

cython_module:
	CPPFLAGS='-DCYTHON_FAST_THREAD_STATE=1' cythonize -X language_level=3 -f -i lib.pyx

clean:
	rm -rf lib.c *.so build/

.PHONY: test cython_module clean
