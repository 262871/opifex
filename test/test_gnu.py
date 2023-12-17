import sys, pathlib
sys.path.append(pathlib.Path.cwd().parent.resolve())

import pytest

from src.opifex import gnu 

@pytest.fixture
def compiler():
    return gnu('c:/msys64/mingw64/bin/g++.exe', 'mingw64')

def test_name(compiler: gnu):
    assert compiler.name == 'mingw64'

def test_path(compiler: gnu):
    assert compiler.path.as_posix() == 'c:/msys64/mingw64/bin/g++.exe'

def test_stages(compiler: gnu):
    assert compiler.outasm == False and compiler.outobj == False and compiler.outfinal == True
    compiler.setstages(True, True, False)
    assert compiler.outasm == True and compiler.outobj == True and compiler.outfinal == False

def test_static(compiler: gnu):
    assert compiler.static == True
    compiler.setstatic(False)
    assert compiler.static == False

def test_includes(compiler: gnu):
    compiler.addincludes('C:/src/VulkanSDK/Include', 'C:/src/volk')
    assert len(compiler.includes) == 2
    compiler.discardincludes('C:/src/volk')
    assert len(compiler.includes) == 1

def test_libpath(compiler: gnu):
    compiler.addlibpaths('c:/src/boost_1_82_0/libs')
    assert len(compiler.libpaths) == 1
    compiler.discardlibpaths('c:/src/boost_1_82_0/libs')
    assert len(compiler.libpaths) == 0

def test_libs(compiler: gnu):
    compiler.addlibs('boost_1_82_0')
    assert len(compiler.libs) == 1
    compiler.discardlibs('boost_1_82_0')
    assert len(compiler.libs) == 0

def test_opts(compiler: gnu):
    compiler.addopts('-O3')
    assert len(compiler.options) == 5
    compiler.discardopts('-pedantic')
    assert len(compiler.options) == 4

@pytest.fixture
def files():
    return [pathlib.Path('mock/main.cpp'), pathlib.Path('mock/app.cxx')]

def test_compile(compiler: gnu, files):
    executable = compiler.compile(files)
    assert executable

def test_safe_path_to_string():
    assert gnu.safe(pathlib.Path('\\test path\\with backslash and spaces')) == '"/test path/with backslash and spaces"'
    
def test_asm_cmd(compiler: gnu, files):
    asm_files, cmd = compiler.asm_cmd(files)
    assert len(cmd) == len('cd "c:/msys64/mingw64/bin" && g++.exe -S "mock/main.cpp" "mock/app.cxx" -I -o "C:/Users/User/Desktop/python/opifex/build/mingw64/asm/main.s" "C:/Users/User/Desktop/python/opifex/build/mingw64/asm/app.s" -Wextra -Wall -Werror -pedantic')
    assert set(asm_files) == {pathlib.Path('build/mingw64/asm/main.s').resolve(), pathlib.Path('build/mingw64/asm/app.s').resolve()}
