import pytest

import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import crawler as crawler

def exists(name):
    op = getattr(crawler, name, None)
    if callable(op):
        return op
    return None

baseSettings = {
    "type": "local",
    "onlyOnce" : "false",
    }

def test_createLocalCrawler():
    settings = baseSettings
    getClassString = lambda x: "<class \'crawler.{}\'>".format(x)
    tests = [
        ["local", "localCrawler"],
        ["google", "googleCrawler"],
        ["git", "gitCrawler"]
    ]
    for test in tests:
        settings["type"] = test[0]
        myCrawler = crawler.createCrawler(settings)
        assert str(myCrawler.__class__) == getClassString(test[1]), "Wrong crawler type was created. Created crawler was: {}".format(type(myCrawler))