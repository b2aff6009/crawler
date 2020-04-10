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
    "extension" : "",
    "service" : False,
    "sleep" : 1,
    "singleReturn" : True 
}

tests = [
    [{"extension": ".csv"}, 5, ["./tests/testdata/test1.csv", "./tests/testdata/test2.csv", "./tests/testdata/test3.csv", "./tests/testdata/test4.csv", "./tests/testdata/test5.csv"]],
    [{"extension": ".xml"}, 2, ["./tests/testdata/test1.xml", "./tests/testdata/test2.xml"]],
    [{"extension": ".json"}, 1, ["./tests/testdata/memo.json"]],
    [{"extension": ""}, 8, []],
    [{"onlyOnce" : False,"extension": ""}, 8, []]
]

def test_find_list():
    settings = baseSettings

    for test in tests:
        for key,val in test[0].items():
            settings[key] = val
        myCrawler = crawler.createCrawler(settings)
        myCrawler.memo = []
        try:
            results = myCrawler.getList()
            assert len(results) == test[1], "Found {} instead of {} {} files".format(len(results), test[1], settings["extension"])
            if len(test[2]) > 0:
                for fileName in results:
                    assert fileName in test[2], "Unexpected file ({}) appeared in found files".format(fileName)
        except ValueError as VE:
            assert settings["onlyOnce"] == False, "Unexpected exeption raises"

def test_find_gen():
    settings = baseSettings

    for test in tests:
        for key,val in test[0].items():
            settings[key] = val
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

singleReturnCnt = 0
def test_callback_singleReturn():
    global singleReturnCnt
    settings = baseSettings
    settings["onlyOnce"] = False
    
    for test in tests:
        for key,val in test[0].items():
            settings[key] = val
        singleReturnCnt = 0 
        def callback (file):
            global singleReturnCnt
            if len(test[2]) > 0:
                assert file in test[2], "Couldn't find file ({}) in {}".format(file, test[2])
            singleReturnCnt +=1

        myCrawler = crawler.createCrawler(settings, callback)
        myCrawler.process()
        assert singleReturnCnt == test[1], "Found {} instead of {} {} files".format(singleReturnCnt, test[1], settings["extension"])    

def test_callback_listReturn():
    settings = baseSettings
    settings["singleReturn"] = False
    
    for test in tests:
        for key,val in test[0].items():
            settings[key] = val
        settings["onlyOnce"] = True
        def callback (files):
            if len(test[2]) > 0:
                for file in files:
                    assert file in test[2], "Couldn't find file ({}) in {}".format(file, test[2])
            assert len(files) == test[1], "Found {} instead of {} {} files".format(len(files), test[1], settings["extension"])

        myCrawler = crawler.createCrawler(settings, callback)
        myCrawler.memo = []
        myCrawler.process()

if __name__ == '__main__':
    test_callback_listReturn()
