import os
import json


def createCrawler(settings, callback = None):
    selector = {
        "local" : localCrawler,
        "google" : googleCrawler,
        "git" : gitCrawler
    }
    return selector[settings.get("type", "local")](settings, callback)

class Crawler:
    def __init__(self, settings, callback = None):
        self.settings = settings
        self.loadMemo()
        self.callback = callback

    def generator(self):
        pass

    def getList(self):
        if(self.settings["onlyOnce"] == True):
            return list(self.generator())
        raise ValueError("onlyOnce option is disabled and would lead to an infinity list")

    def loadMemo(self):
        if self.settings["onlyOnce"] == True:
           with open(self.settings["memo"], 'rb') as f:
               self.memo = json.load(f) 
        else:
            self.memo = []

    def save(self):
        with open(self.settings["memo"], 'w') as f:
            json.dump(self.memo, f, indent = 4)

    def process(self):
        pass

class localCrawler(Crawler):
    def __init__(self, settings, callback = None):
        super().__init__(settings, callback)

    def generator(self):
        for subdir, dirs, files in os.walk(self.settings["path"]):
            for filename in files:
                if (filename.endswith(self.settings["extension"])):
                    filepath = os.path.join(subdir, filename)
                    if (self.settings["onlyOnce"] == False or filepath not in self.memo):
                        #result.append([os.path.join(subdir, filename), filename.replace(self.settings["extension"],""), subdir.split("/")[-1]])
                        self.memo.append(filepath)
                        self.save()
                        yield filepath

    def process(self):
        if self.settings["singleReturn"] == True:
            for file in self.generator():
                self.callback(file)
        else:
            self.callback(self.getList())
        pass

class googleCrawler(Crawler):
    def __init__(self, settings, callback = None):
        super().__init__(settings)

class gitCrawler(Crawler):
    def __init__(self, settings, callback = None):
        super().__init__(settings)