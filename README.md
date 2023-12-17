![Tests - Passing](https://img.shields.io/static/v1?label=Tests&message=Passing&color=2ea44f&logo=github&logoColor=%23d8d8d8)
![Coverage - 100%](https://img.shields.io/static/v1?label=Coverage&message=100%&color=2ea44f&logo=pytest&logoColor=%23d8d8d8)
# opifex
Accelerates configuration and usage of compilers from python.

## Tests
### pytest
```
test/test_gnu.py::test_name PASSED                                                      [  9%]
test/test_gnu.py::test_path PASSED                                                      [ 18%]
test/test_gnu.py::test_stages PASSED                                                    [ 27%]
test/test_gnu.py::test_static PASSED                                                    [ 36%]
test/test_gnu.py::test_includes PASSED                                                  [ 45%]
test/test_gnu.py::test_libpath PASSED                                                   [ 54%]
test/test_gnu.py::test_libs PASSED                                                      [ 63%]
test/test_gnu.py::test_opts PASSED                                                      [ 72%]
test/test_opifex.py::test_pytest PASSED                                                 [ 81%]
test/test_opifex.py::test_opifex PASSED                                                 [ 90%]
test/test_opifex.py::test_gnu PASSED                                                    [100%]

===================================== 11 passed in 0.11s =====================================
```
### coverage
```
Name                     Stmts   Miss  Cover
--------------------------------------------
src\opifex\__init__.py       1      0   100%
src\opifex\gnu\gnu.py       65      0   100%
test\test_gnu.py            39      0   100%
test\test_opifex.py          9      0   100%
--------------------------------------------
TOTAL                      114      0   100%
```
