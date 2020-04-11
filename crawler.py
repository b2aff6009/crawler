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
        raise ValueError("onlyOnce option is disabled, this would lead to an infinity list")

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
        if self.callback == None:
            raise ValueError("Callback function is not defined, which is needed to the process call. You might want to use generator() instead.")
        if self.settings["singleReturn"] == True:
            for file in self.generator():
                self.callback(file)
        else:
            self.callback(self.getList())

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
        #self.reader = googleApi.GoogleSheetApi(self.settings.get("googleApi"))
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
