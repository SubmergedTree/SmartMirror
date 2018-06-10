import unittest
from html_builder import HtmlBuilder
from root_dir import ROOT_DIR

INDEX = ROOT_DIR + '/tests/test_html_builder_data/html/index.html'
JS_PATH = ROOT_DIR + '/tests/test_html_builder_data/js'
HTML_PATH = ROOT_DIR + '/tests/test_html_builder_data/html'
RESULT_PATH = ROOT_DIR + '/tests/test_html_builder_data/result_html.html'


class HtmlBuilderTest(unittest.TestCase):

    def test_build(self):
        html_builder = HtmlBuilder(JS_PATH, HTML_PATH, INDEX)
        result = html_builder.build_html()
        with open(RESULT_PATH) as fh:
            should = fh.read()
        self.assertEqual(should, result)
