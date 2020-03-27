import os


def createCrawler(settings):
    selector = {
        "local" : localCrawler,
        "google" : googleCrawler,
        "git" : gitCrawler
    }
    return selector[settings.get("type", "local")](settings)

class Crawler:
    def __init__(self, settings):
        self.settings = settings

class localCrawler(Crawler):
    def __init__(self, settings):
        pass

class googleCrawler(Crawler):
    def __init__(self, settings):
        pass

class gitCrawler(Crawler):
    def __init__(self, settings):
        pass