import json
from root_dir import ROOT_DIR
from util.logger import Logger

class UrlMapping:
    def __init__(self, widget, url):
        self.widget = widget
        self.url = url


class UrlLoader:

    def load_urls(self, relative_path):
        path = ROOT_DIR + relative_path
        urls = []
        try:
            with open(path, 'r') as fh:
                loaded = json.load(fh)
                
        except (IOError, KeyError, ValueError) as e:
            Logger.warn("Malformed or missing url.json. {}".format(e))


