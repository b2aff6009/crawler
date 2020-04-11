import pytest

import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import crawler as crawler

import testutils as tu

baseSettings = {
    "type": "local",
    "memo" : "./tests/testdata/memo.json",
    "onlyOnce" : True,
    "path" : "./tests/testdata/",
    "extension" : "",
    "service" : False,
    "sleep" : 1,
    "singleReturn" : True 
}

tests = [
    [{"extension": ".csv"}, 5, ["./tests/testdata/test1.csv",
                                "./tests/testdata/test2.csv", 
                                "./tests/testdata/test3.csv", 
                                "./tests/testdata/test4.csv", 
                                "./tests/testdata/test5.csv"]],

    [{"extension": ".xml"}, 2, ["./tests/testdata/test1.xml", 
                                "./tests/testdata/test2.xml"]],

    [{"extension": ".json"}, 1, ["./tests/testdata/memo.json"]],

    [{"extension": ""}, 8, ["./tests/testdata/test1.csv",
                            "./tests/testdata/test2.csv",
                            "./tests/testdata/test3.csv",
                            "./tests/testdata/test4.csv", 
                            "./tests/testdata/test5.csv",
                            "./tests/testdata/test1.xml",
                            "./tests/testdata/test2.xml",
                            "./tests/testdata/memo.json"]],
    [{"onlyOnce" : False,"extension": ""}, 8, ["./tests/testdata/test1.csv",
                            "./tests/testdata/test2.csv",
                            "./tests/testdata/test3.csv",
                            "./tests/testdata/test4.csv", 
                            "./tests/testdata/test5.csv",
                            "./tests/testdata/test1.xml",
                            "./tests/testdata/test2.xml",
                            "./tests/testdata/memo.json"]]
]

def test_find_list():
    tu.find_list(baseSettings, tests)

def test_find_gen():
    tu.find_gen(baseSettings, tests)


def test_callback_singleReturn():
    tu.callback_singleReturn(baseSettings, tests)

def test_callback_listReturn():
    tu.callback_listReturn(baseSettings, tests)

if __name__ == '__main__':
    test_callback_singleReturn()
