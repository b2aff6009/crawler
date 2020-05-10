import pytest

import os
import sys
import inspect
import json
import datetime 
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import crawler as crawler

baseSettings = {
    "type": "local",
    "memo" : "./tests/testdata/memo.json",
    "onlyOnce" : True,
    #LocalCrawler Settings
    "path" : "./tests/testdata/",
    "extension" : "",
    #GoogleCrawler Settings
    "credentialPath" : "./dummy-credentials.json",
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

cnt = 0
def test_service():
    global cnt
    settings = baseSettings
    settings["service"] = True
    settings["sleep"] = 1
    settings["onlyOnce"] = True
    cnt = 0
    mId = 3
    cycles = 10

    def callback(file, id, processingCrawler):
        global cnt
        cnt = cnt + 1
        assert id == mId, "Argurments doesn't match the expected. Got {} instead of {}".format(id, mId)
        if cnt >= cycles:   
            processingCrawler.settings["service"] = False

    mCrawler = crawler.createCrawler(settings, callback)
    startTime = datetime.datetime.now()
    mCrawler.process(mId, mCrawler)
    endTime = datetime.datetime.now()
    diffTime = endTime - startTime
    def checkTime(seconds):
        if seconds > (cycles-1)*settings["sleep"] and seconds < (cycles+1)*settings["sleep"]:
            return True
        return False

    assert checkTime(diffTime.seconds), "Test took {}s, expceted time would be {}s".format(diffTime.seconds, cycles*settings["sleep"])
    assert cnt == cycles, "Wrong number of cycles. Got {} instead of {}".format(cnt, cycles)

        
if __name__ == "__main__":
    #test_createCrawlerFactory()
    test_service()