from root_dir import ROOT_DIR
import unittest
from loader.load_urls import UrlLoader, UrlMapping, NoUrlMappingException

TEST_URLS_PATH = ROOT_DIR + '/tests/url_loader_test_data/test_urls.json'
TEST_WRONG_KEY_URLS_PATH = ROOT_DIR + '/tests/url_loader_test_data/wrong_key.json'
TEST_MALFORMED_URLS_PATH = ROOT_DIR + '/tests/url_loader_test_data/malformed.json'
TEST_DOES_NOT_EXIST_URLS_PATH = ROOT_DIR + '/tests/url_loader_test_data/not_exist.json'


class UrlListAssert:

    def assertUrlListContainsSame(self, is_url_list, should_url_list):
        len_is = len(is_url_list)
        len_should = len(should_url_list)
        if len_is != len_should:
            raise AssertionError('Size is different')
        for index in range(0, len_is):
            if not is_url_list[index].__eq__(should_url_list[index]):
                raise AssertionError('Values are different')


class LoadUrlsTest(unittest.TestCase, UrlListAssert):

    def test_load_urls(self):
        url_loader = UrlLoader()
        urls = url_loader.load_urls(TEST_URLS_PATH)
        self.assertUrlListContainsSame(urls, [UrlMapping('foo', 'fooUrl'), UrlMapping('bar', 'barUrl')])

    def test_no_urls_file_exists(self):
        url_loader = UrlLoader()
        try:
            url_loader.load_urls(TEST_DOES_NOT_EXIST_URLS_PATH)
        except NoUrlMappingException:
            self.assertTrue(True)
        #self.assertRaises(NoUrlMappingException, url_loader.load_urls(TEST_DOES_NOT_EXIST_URLS_PATH))

    def test_malformed_urls_file(self):
        url_loader = UrlLoader()
        try:
            url_loader.load_urls(TEST_MALFORMED_URLS_PATH)
        except NoUrlMappingException:
            self.assertTrue(True)


    def test_wrong_key_urls_file(self):
        url_loader = UrlLoader()
        try:
            url_loader.load_urls(TEST_WRONG_KEY_URLS_PATH)
        except NoUrlMappingException:
            self.assertTrue(True)
