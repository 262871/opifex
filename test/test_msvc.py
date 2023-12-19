import pytest

from opifex import msvc


@pytest.fixture
def compiler():
    return msvc('C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat', 'msvc64')

def test_name(compiler: msvc):
    assert compiler.name == 'msvc64'

def test_path(compiler: msvc):
    assert compiler.path.as_posix() == 'C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvars64.bat'
    