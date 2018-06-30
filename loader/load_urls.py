import json
from root_dir import ROOT_DIR
from util.logger import Logger


class NoUrlMappingException(Exception):
    def __init__(self):
        pass

class UrlMapping:
    def __init__(self, widget, url):
        self.widget = widget
        self.url = url

    def __eq__(self, other):
        return self.widget == other.widget and self.url == other.url

class UrlLoader:

    def load_urls(self, path):
        urls = []
        try:
            with open(path, 'r') as fh:
                loaded = json.load(fh)
                for item in loaded:
                    urls.append(UrlMapping(item['widget'], item['url']))
        except Exception as e:
            Logger.warn("Unable to parse urls.json: {}".format(e))
            raise NoUrlMappingException()
        return urls
