import pytest

import os
import sys
import inspect
import json
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

def test_createCrawlerFactory():
    settings = baseSettings
    
    tests = [
        ["local", crawler.localCrawler],
        ["google", crawler.googleCrawler],
        ["git", crawler.gitCrawler]
    ]
    for test in tests:
        settings["type"] = test[0]
        myCrawler = crawler.createCrawler(settings)
        testCrawler = test[1](settings)
        assert type(myCrawler) ==  type(testCrawler),"Wrong crawler type was created. Created crawler was: {}".format(type(myCrawler))

def test_save():
    dummyName = "dummyMemo"
    mCrawler = crawler.createCrawler(baseSettings)
    mCrawler.memo.append(dummyName)
    mCrawler.save()
    with open(baseSettings["memo"], 'rb') as f:
        data = json.load(f)
    assert dummyName in data, "Didn't found {} in {}".format(dummyName, baseSettings["memo"]) 

def test_load():
    dummyName = "dummyLoad"
    data = [dummyName]
    with open(baseSettings['memo'], 'w') as f:
        json.dump(data, f, indent=4)
    mCrawler = crawler.createCrawler(baseSettings)
    assert len(mCrawler.memo) == 1, "Crawler memo contains not exactly one item"
    assert mCrawler.memo[0] == dummyName, "Crawlers memo contains {} instead of {}".format(mCrawler.memo[0], dummyName) 


if __name__ == "__main__":
    test_load()