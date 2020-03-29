import pytest

import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import crawler as crawler

baseSettings = {
    "type": "local",
    "memo" : "./tests/testdata/memo.json",
    "onlyOnce" : True,
    "path" : "./tests/testdata/",
    "extension" : ""
    }

def test_find_list():
    settings = baseSettings
    tests = [
        [{"extension": ".csv"}, 5, []],
        [{"extension": ".xml"}, 2, ["./tests/testdata/test1.xml", "./tests/testdata/test2.xml"]],
        [{"extension": ".json"}, 1, ["./tests/testdata/memo.json"]],
        [{"extension": ""}, 8, []],
        [{"onlyOnce" : False,"extension": ""}, 8, []]
    ]
    for test in tests:
        for key,val in test[0].items():
            settings[key] = val
        myCrawler = crawler.createCrawler(settings)
        myCrawler.memo = []
        try:
            results = myCrawler.list()
            assert len(results) == test[1], "Found {} instead of {} {} files".format(len(results), test[1], settings["extension"])
            if len(test[2]) > 0:
                for fileName in results:
                    assert fileName in test[2], "Unexpected file ({}) appeared in found files".format(fileName)
        except ValueError as VE:
            assert settings["onlyOnce"] == False, "Unexpected exeption raises"

def test_find_gen():
    settings = baseSettings

    tests = [
        [".csv", 5, []],
        [".xml", 2, ["./tests/testdata/test1.xml", "./tests/testdata/test2.xml"]],
        [".json", 1, ["./tests/testdata/memo.json"]],
        ["", 8, []]
    ]
    for test in tests:
        settings["extension"] = test[0]
        myCrawler = crawler.createCrawler(settings)
        myCrawler.memo = []
        gen = myCrawler.generator()
        cnt = 0
        try:
            while True:
                fileName = next(gen)
                if len(test[2]) > 0:
                    assert fileName in test[2], "Unexpected file ({}) appeared in found files".format(fileName)
                cnt += 1
        except StopIteration:
            assert cnt == test[1], "Found {} instead of {} {} files".format(cnt, test[1], test[0])

if __name__ == '__main__':
    test_find_gen()
