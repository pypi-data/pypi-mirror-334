#!/usr/bin/env python3
# -fire CLI
from fire import Fire
from nuphy2.version import __version__

#print("D... module nuphy2/react is being run")


def func():
    print("D... function defined in nuphy2:react")
    return True

def test_func():
    print("D... test function ... run pytest")
    assert func()==True



if __name__=="__main__":
    print("D... in main of project/module:  nuphy2/react ")
    print("D... version :", __version__ )
    Fire(  )
