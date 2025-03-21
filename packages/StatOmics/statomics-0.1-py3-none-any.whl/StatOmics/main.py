# main.py

from .r_interface import run_test as _run_test

def test(string):
    return _run_test(string)
