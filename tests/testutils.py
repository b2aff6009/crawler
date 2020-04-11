import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import crawler as crawler

def find_gen(baseSettings, tests):
    for i, test in enumerate(tests):
        settings = baseSettings
        for key,val in test[0].items():
            settings[key] = val
        myCrawler = crawler.createCrawler(settings)
        myCrawler.memo = []
        gen = myCrawler.generator()
        cnt = 0
        results = []
        try:
            while True:
                name = next(gen)
                results.append(name)
                assert name in test[2], "Unexpected file ({}) appeared in found files. During Test: {}".format(name, i)
                cnt += 1
        except StopIteration:
            assert cnt == test[1], "Found {} instead of {} {} files".format(cnt, test[1], test[0])

def find_list(baseSettings, tests):
    for i,test in enumerate(tests):
        settings = baseSettings
        for key,val in test[0].items():
            settings[key] = val
        myCrawler = crawler.createCrawler(settings)
        myCrawler.memo = []
        try:
            results = myCrawler.getList()
            assert len(results) == test[1], "Found {} instead of {} files".format(len(results), test[1])
            if len(test[2]) > 0:
                for name in results:
                    assert name in test[2], "Unexpected file ({}) in Test {} appeared in found files. Expected {}".format(name, i, test[2])
        except ValueError as VE:
            assert settings["onlyOnce"] == False, "Unexpected exeption raises"

singleReturnCnt = 0
def callback_singleReturn(baseSettings, tests):
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
        assert singleReturnCnt == test[1], "Found {} instead of {} files".format(singleReturnCnt, test[1])


def callback_listReturn(baseSettings, tests):
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
            assert len(files) == test[1], "Found {} instead of {} files".format(len(files), test[1]) 

        myCrawler = crawler.createCrawler(settings, callback)
        myCrawler.memo = []
        myCrawler.process()


