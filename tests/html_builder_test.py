import unittest
from html_builder import HtmlBuilder


class HtmlBuilderTest(unittest.TestCase):

    def setUp(self):
        self.html_builder = HtmlBuilder('tests/test_html_builder_data/js', 'tests/test_html_builder_data/html')

