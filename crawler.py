import os
import json
import time
import sys


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
        self.debug = settings.get("debug",0)
        self.loadMemo()
        self.callback = callback
        if self.debug > 0:
            print("Crawler: initilised.")

    def generator(self):
        if self.debug > 2:
            print("Crawler: Generator") 
        pass

    def getList(self):
        if(self.settings["onlyOnce"] == True):
            return list(self.generator())
        raise ValueError("onlyOnce option is disabled, this would lead to an infinity list")

    def loadMemo(self):
        if self.settings["onlyOnce"] == True:
            if self.debug > 2:
                print("Crawler: read Memo.")
            if os.path.isfile(self.settings["memo"]) == False:
                self.memo = []
                with open(self.settings["memo"], 'w+') as f:
                    json.dump(self.memo, f, indent = 4)

            with open(self.settings["memo"], 'rb') as f:
                self.memo = json.load(f) 
        else:
            self.memo = []

    def save(self):
        with open(self.settings["memo"], 'w') as f:
            json.dump(self.memo, f, indent = 4)

    def process(self, *args):
        if self.callback == None:
            raise ValueError("Callback function is not defined, which is needed to the process call. You might want to use generator() instead.")
        firstRun = True
        if self.debug > 0:
            print("Crawler: process")
        while self.settings.get("service", False) or firstRun:
            firstRun = False
            try:
                if self.settings.get("singleReturn",False) == True:
                    for myfile in self.generator():
                        if self.debug > 3:
                            print("Crawler: fire callback with file: {}".format(myfile))
                        self.callback(myfile, *args)
                else:
                    files = self.getList()
                    if self.debug > 3:
                        print("Crawler: fire callback with files: {}".format(", ".join(files)))
                    self.callback(files, *args)
                time.sleep(self.settings.get("sleep", 1))
            except:
                print("Oops!", sys.exc_info()[0], "occured.")
                time.sleep(self.settings.get("sleep", 1)*10)

class localCrawler(Crawler):
    def __init__(self, settings, callback = None):
        super().__init__(settings, callback)

    def generator(self):
        super().generator()
        if self.debug > 3:
            print("Crawler: local crawls thru {}".format(self.settings["path"])) 
        for subdir, dirs, files in os.walk(self.settings["path"]):
            for filename in files:
                if self.debug > 5:
                    print("Crawler: Test file {}".format(filename))
                if (filename.lower().endswith(self.settings["extension"].lower())):
                    filepath = os.path.join(subdir, filename)
                    if self.debug > 4:
                        print("Crawler: found file {}".format(filepath))
                    if (self.settings["onlyOnce"] == False or filepath not in self.memo):
                        self.memo.append(filepath)
                        self.save()
                        if self.debug > 4:
                            print("Crawler: yield file {}".format(filepath))
                        yield filepath


import gspread 
from oauth2client.service_account import ServiceAccountCredentials
class googleCrawler(Crawler):
    def __init__(self, settings, callback = None):
        super().__init__(settings, callback)
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(settings["credentialPath"], self.scope)
        self.client = gspread.authorize(self.creds)

    def generator(self):
        sheets = self.client.openall()
        for sheet in sheets:
            if (self.settings["spreadsheets"] not in sheet.title):
                continue

            if (self.settings["enableWorksheets"] == False):
                if (self.settings["returnType"] == "path"):
                    yield sheet.title
                else:
                    yield sheet
            else:
                for worksheet in sheet.worksheets():
                    if (self.settings["worksheets"] not in worksheet.title):
                        continue
                    if (self.settings["returnType"] == "path"):
                        yield sheet.title + "/" + worksheet.title
                    else:
                        yield worksheet

    def search(self):
        sheets = self.client.openall()
        self.reader.setFile(self.settings.get("path"))
        self.sheets = self.reader.getSheets()
        result = []
        for sheet in self.sheets:
            if sheet not in self.settings["skip"]:
                if self.settings["onlyOnce"] == False or sheet not in self.memo.get("files"):
                    self.memo.get("files").append(sheet)
                    result.append(sheet)
        self.dumpMemo()
        return result

class gitCrawler(Crawler):
    def __init__(self, settings, callback = None):
        super().__init__(settings)
