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
test/test_gnu.py::test_name PASSED                                       [  3%]
test/test_gnu.py::test_path PASSED                                       [  6%]
test/test_gnu.py::test_stages PASSED                                     [  9%]
test/test_gnu.py::test_static PASSED                                     [ 12%]
test/test_gnu.py::test_includes PASSED                                   [ 16%]
test/test_gnu.py::test_libpath PASSED                                    [ 19%]
test/test_gnu.py::test_libs PASSED                                       [ 22%]
test/test_gnu.py::test_opts PASSED                                       [ 25%]
test/test_gnu.py::test_async_compile PASSED                              [ 32%]
test/test_gnu.py::test_asm_command PASSED                                [ 38%]
test/test_gnu.py::test_obj_command PASSED                                [ 41%]
test/test_gnu.py::test_final_command PASSED                              [ 45%]
test/test_gnu.py::test_compile_kernel PASSED                             [ 48%]
test/test_gnu.py::test_async_compile_kernel PASSED                       [ 51%]
test/test_gnu.py::test_create_env PASSED                                 [ 54%]
test/test_gnu.py::test_create_prefix PASSED                              [ 58%]
test/test_msvc.py::test_name PASSED                                      [ 61%]
test/test_msvc.py::test_path PASSED                                      [ 64%]
test/test_msvc.py::test_stages PASSED                                    [ 67%]
test/test_msvc.py::test_static PASSED                                    [ 70%]
test/test_msvc.py::test_includes PASSED                                  [ 74%]
test/test_msvc.py::test_libpath PASSED                                   [ 77%]
test/test_msvc.py::test_defaultlibs PASSED                               [ 80%]
test/test_msvc.py::test_nodefaultlibs PASSED                             [ 83%]
test/test_msvc.py::test_opts PASSED                                      [ 87%]
test/test_opifex.py::test_pytest PASSED                                  [ 90%]
test/test_opifex.py::test_opifex PASSED                                  [ 93%]
test/test_opifex.py::test_gnu PASSED                                     [ 96%]
test/test_opifex.py::test_msvc PASSED                                    [100%]

============================= 31 passed in 0.41s ==============================
```
### coverage
```
Name                      Stmts   Miss  Cover
---------------------------------------------
src\opifex\__init__.py        2      0   100%
src\opifex\gnu\gnu.py       167      0   100%
src\opifex\msvc\msvc.py      78      0   100%
test\test_gnu.py            105      0   100%
test\test_msvc.py            42      0   100%
test\test_opifex.py           9      0   100%
---------------------------------------------
TOTAL                       403      0   100%
```
