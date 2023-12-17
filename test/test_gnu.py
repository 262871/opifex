import sys, pathlib
sys.path.append(pathlib.Path.cwd().parent.resolve())

import pytest

import src.opifex.gnu as gnu

@pytest.fixture
def compiler():
    return gnu('c:/msys64/mingw64/bin/g++.exe', 'mingw64')

def test_name(compiler):
    assert compiler.name == 'mingw64'

def test_path(compiler):
    assert compiler.path.as_posix() == 'c:/msys64/mingw64/bin/g++.exe'

def test_includes(compiler):
    compiler.addincludes('C:/src/VulkanSDK/Include', 'C:/src/volk')
    assert len(compiler.includes) == 2
    compiler.discardincludes('C:/src/volk')
    assert len(compiler.includes) == 1

def test_stages(compiler):
    assert compiler.outasm == False and compiler.outobj == False and compiler.outfinal == True
    compiler.setstages(True, True, False)
    assert compiler.outasm == True and compiler.outobj == True and compiler.outfinal == False

def test_static(compiler):
    assert compiler.static == True
    compiler.setstatic(False)
    assert compiler.static == False
