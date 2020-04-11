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
    "type": "google",
    "memo" : "./tests/testdata/memo.json",
    "onlyOnce" : True,
    "service" : False,
    "sleep" : 1,
    "singleReturn" : True,
    #google specific settings
    "credentialPath" : "./dummy-credentials.json",
    "spreadsheets" : "",
    "worksheets": "",
    "enableWorksheets": False,
    "returnType" : "path" 
}

tests = [
    [{"enableWorksheets": False, "spreadsheets": "", "worksheets": ""}, 2, ["Dummy1", "Dummy2"]],
    [{"enableWorksheets": False, "spreadsheets": "1", "worksheets": ""}, 1, ["Dummy1"]],
    [{"enableWorksheets": True, "spreadsheets": "", "worksheets": ""}, 5, ["Dummy1/Test1", "Dummy1/Test2","Dummy1/Test3", "Dummy2/Sheet1","Dummy2/Sheet2" ]],
    [{"enableWorksheets": True, "spreadsheets": "1", "worksheets": ""}, 3, ["Dummy1/Test1", "Dummy1/Test2","Dummy1/Test3"]],
    [{"enableWorksheets": True, "spreadsheets": "", "worksheets": "1"}, 2, ["Dummy1/Test1", "Dummy2/Sheet1"]],
    [{"enableWorksheets": True, "spreadsheets": "1", "worksheets": "1"}, 1, ["Dummy1/Test1"]],
]

def test_create_google_crawler():
    settings = baseSettings
    crawler.createCrawler(settings)

def test_find_gen():
    tu.find_gen(baseSettings, tests)

def test_find_list():
    tu.find_list(baseSettings, tests)

def test_callback_singleReturn():
    tu.callback_singleReturn(baseSettings, tests)

def test_callback_listReturn():
    tu.callback_listReturn(baseSettings, tests)

if __name__ == '__main__':
    test_callback_listReturn()