import pytest

from opifex import msvc


@pytest.fixture
def compiler():
    return msvc('C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat', 'msvc64')

def test_name(compiler: msvc):
    assert compiler.name == 'msvc64'

def test_path(compiler: msvc):
    assert compiler.path.as_posix() == 'C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvars64.bat'
    
def test_stages(compiler: msvc):
    assert compiler.outasm == False and compiler.outobj == False and compiler.outfinal == True
    compiler.setstages(True, True, False)
    assert compiler.outasm == True and compiler.outobj == True and compiler.outfinal == False

def test_static(compiler: msvc):
    assert compiler.static == True
    compiler.setstatic(False)
    assert compiler.static == False
