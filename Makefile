test: cython_module
	command time python test.py 10
	command time python test.py 20

cython_module:
	cythonize -i lib.pyx

clean:
	rm -rf lib.c *.so build/

.PHONY: test cython_module clean
