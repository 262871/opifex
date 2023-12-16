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
    return gnu('mingw64')

def test_name(compiler):
    assert compiler.name == 'mingw64'
