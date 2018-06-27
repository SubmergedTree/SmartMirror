from root_dir import ROOT_DIR
import unittest
from loader.load_urls import UrlLoader

TEST_URLS_PATH = ROOT_DIR + '/tests/url_loader_test_data/test_urls.json'
TEST_WRONG_KEY_URLS_PATH = ROOT_DIR + '/tests/url_loader_test_data/wrong_key.json'
TEST_MALFORMED_URLS_PATH = ROOT_DIR + '/tests/url_loader_test_data/malformed.json'


class ShouldList:
    def __init__(self, widgets, urls):
        self.widgets = widgets
        self.urls = urls

    def __contains__(self, item):
        widget_pos = None
        urls_pos = None
        if item.widget in self.widgets:
            widget_pos = self.widgets.index(item.widget)
        if item.url in self.urls:
            urls_pos = self.urls.index(item.url)
        if not (widget_pos and urls_pos and widget_pos == urls_pos):
            raise AssertionError('widget: {} / url: {} shall not exist'.format(item.widget, item.url))


class UrlListAssert:

    def assertUrlListContainsSame(self, url_list, should_widgets, should_urls):
        s = ShouldList(should_widgets, should_urls)
        for item in url_list:
            if item.widget not in s:
                raise AssertionError('{} not in second list'.format(item))


class LoadUrlsTest(unittest.TestCase, UrlListAssert):

    def test_load_urls(self):
        url_loader = UrlLoader()
        urls = url_loader.load_urls(TEST_URLS_PATH)
        self.assertUrlListContainsSame(urls, ['foo', 'bar'], ['fooUrl', 'barUrl'])

    def test_no_urls_file_exists(self):
        pass

    def test_malformed_urls_file(self):
        pass

    def test_wrong_key_urls_file(self):
        pass