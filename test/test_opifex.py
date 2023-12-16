import sys, pathlib
sys.path.append(pathlib.Path.cwd().parent.resolve())

import pytest

import src.opifex as opifex
import src.opifex.gnu as gnu

def test_pytest():
    assert True

def test_opifex():
    assert opifex

def test_gnu():
    assert gnu

@pytest.fixture
def compiler():
    return gnu('c:/msys64/mingw64/bin/g++.exe', 'mingw64')

def test_name(compiler):
    assert compiler.name == 'mingw64'

def test_path(compiler):
    assert compiler.path.as_posix() == 'c:/msys64/mingw64/bin/g++.exe'
