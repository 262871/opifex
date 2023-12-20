![Tests - Passing](https://img.shields.io/static/v1?label=Tests&message=Passing&color=2ea44f&logo=github&logoColor=%23d8d8d8)
![Coverage - 100%](https://img.shields.io/static/v1?label=Coverage&message=100%&color=2ea44f&logo=pytest&logoColor=%23d8d8d8)
# opifex
Accelerates configuration and usage of compilers from python.

## Quickstart
opifex is designed to be convenient and easy to use while promoting correct use. There are many different ways of accessing most of its functionality. To get started, simply import opifex and create a compiler object by providing the filepath to it along with a tool chain name to distinguish it from other compiler configurations. You can optionally use named key word arguments to configure the compiler immediately upon creation, or you may use functions such as addincludes(*includes) or addopts(*opts) to add one or many of each configuration. These functions can also be chained if you prefer.
```
# ...
gcc = gnu('c:/msys64/mingw64/bin/g++.exe', 'mingw64')

gcc.addincludes(['C:/src/VulkanSDK/Include', 'C:/src/volk'])
gcc.setstages(asm=True, obj=False, final=True)

# Default options are {'-Wall', '-Wextra', '-pedantic', '-Werror'}
# and {'/W4', '/EHsc', '/options:strict'} on msvc
# '-static' is separate and disabled by calling .setstatic(False)
gcc.addopts('-O3').discardopts('-pedantic')

# Here 'files' would be the cpp files of the project
program_filepath, compiler_output = gcc.compile(files)
for ret_code, stdout, stderr in compiler_output:
    print(stdout)
    print(stderr)
# ...
```

## Tests
### pytest
```
test/test_gnu.py::test_name PASSED                                       [  4%]
test/test_gnu.py::test_path PASSED                                       [  9%]
test/test_gnu.py::test_stages PASSED                                     [ 14%]
test/test_gnu.py::test_static PASSED                                     [ 19%]
test/test_gnu.py::test_includes PASSED                                   [ 23%]
test/test_gnu.py::test_libpath PASSED                                    [ 28%]
test/test_gnu.py::test_libs PASSED                                       [ 33%]
test/test_gnu.py::test_opts PASSED                                       [ 38%]
test/test_gnu.py::test_compile PASSED                                    [ 42%]
test/test_gnu.py::test_async_compile PASSED                              [ 47%]
test/test_gnu.py::test_safe PASSED                                       [ 52%]
test/test_gnu.py::test_asm_command PASSED                                [ 57%]
test/test_gnu.py::test_obj_command PASSED                                [ 61%]
test/test_gnu.py::test_final_command PASSED                              [ 66%]
test/test_gnu.py::test_compile_kernel PASSED                             [ 71%]
test/test_gnu.py::test_async_compile_kernel PASSED                       [ 76%]
test/test_gnu.py::test_create_env PASSED                                 [ 80%]
test/test_gnu.py::test_create_prefix PASSED                              [ 85%]
test/test_opifex.py::test_pytest PASSED                                  [ 90%]
test/test_opifex.py::test_opifex PASSED                                  [ 95%]
test/test_opifex.py::test_gnu PASSED                                     [100%]

============================= 21 passed in 0.50s ==============================
```
### coverage
```
Name                     Stmts   Miss  Cover
--------------------------------------------
src\opifex\__init__.py       1      0   100%
src\opifex\gnu\gnu.py      167      0   100%
test\test_gnu.py           108      0   100%
test\test_opifex.py          9      0   100%
--------------------------------------------
TOTAL                      285      0   100%
```
