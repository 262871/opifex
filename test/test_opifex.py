import sys, pathlib
sys.path.append(pathlib.Path.cwd().parent.resolve())

import src.opifex as opifex

def test_pytest():
    assert True

def test_opifex():
    assert opifex
