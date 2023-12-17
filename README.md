![Tests - Passing](https://img.shields.io/static/v1?label=Tests&message=Passing&color=2ea44f&logo=github&logoColor=%23d8d8d8)
![Coverage - 100%](https://img.shields.io/static/v1?label=Coverage&message=100%&color=2ea44f&logo=pytest&logoColor=%23d8d8d8)
# opifex
Accelerates configuration and usage of compilers from python.

## Tests
### pytest
```
test/test_gnu.py::test_name PASSED                   [  5%]
test/test_gnu.py::test_path PASSED                   [ 11%]
test/test_gnu.py::test_stages PASSED                 [ 17%]
test/test_gnu.py::test_static PASSED                 [ 23%]
test/test_gnu.py::test_includes PASSED               [ 29%]
test/test_gnu.py::test_libpath PASSED                [ 35%]
test/test_gnu.py::test_libs PASSED                   [ 41%]
test/test_gnu.py::test_opts PASSED                   [ 47%]
test/test_gnu.py::test_compile PASSED                [ 52%]
test/test_gnu.py::test_safe_path_to_string PASSED    [ 58%]
test/test_gnu.py::test_asm_cmd PASSED                [ 64%]
test/test_gnu.py::test_obj_cmd PASSED                [ 70%]
test/test_gnu.py::test_final_cmd PASSED              [ 76%]
test/test_gnu.py::test_compile_kernel PASSED         [ 82%]
test/test_opifex.py::test_pytest PASSED              [ 88%]
test/test_opifex.py::test_opifex PASSED              [ 94%]
test/test_opifex.py::test_gnu PASSED                 [100%]

=================== 17 passed in 0.17s ====================
```
### coverage
```
Name                     Stmts   Miss  Cover
--------------------------------------------
src\opifex\__init__.py       1      0   100%
src\opifex\gnu\gnu.py      123      0   100%
test\test_gnu.py            66      0   100%
test\test_opifex.py          9      0   100%
--------------------------------------------
TOTAL                      199      0   100%
```
