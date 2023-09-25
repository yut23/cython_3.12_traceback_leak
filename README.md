To reproduce:
1. Install Cython >= 3.0.0 and CPython >= 3.12.0a6
1. Run `make test`
2. Observe the increase in max resident memory between the two runs with different iteration counts (should be +1MiB per iteration).

Cython 3.0.2 and CPython 3.12.0rc3:
```
cythonize -i lib.pyx
command time python test.py 10
10/10
0.04user 0.01system 0:00.06elapsed 96%CPU (0avgtext+0avgdata 21696maxresident)k
0inputs+0outputs (0major+3934minor)pagefaults 0swaps
command time python test.py 20
20/20
0.03user 0.02system 0:00.06elapsed 97%CPU (0avgtext+0avgdata 31872maxresident)k
0inputs+0outputs (0major+6507minor)pagefaults 0swaps
```

Cython 3.0.2 and CPython 3.11.5:
```
cythonize -i lib.pyx
command time python test.py 10
10/10
0.03user 0.00system 0:00.04elapsed 95%CPU (0avgtext+0avgdata 11740maxresident)k
0inputs+0outputs (0major+1875minor)pagefaults 0swaps
command time python test.py 20
20/20
0.01user 0.00system 0:00.02elapsed 95%CPU (0avgtext+0avgdata 12132maxresident)k
0inputs+0outputs (0major+1875minor)pagefaults 0swaps
```
