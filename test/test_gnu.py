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
