import unittest
from widget.widget_resolver import WidgetResolver
from widget.widget import Widget
from database.database import WidgetUser

url_mock = 'www.example.com/rest'

class WidgetDaoMock:
    def get_base_url(self, widget):
        return url_mock


class WidgetUserDaoMock:
    def get_mapping(self, username):
        w = WidgetUser()
        w.mapping_id = 1
        w.position = 2
        w.context = 'Context: 123'
        if username == 'Fib':
            w.widget = "GenericWidget"
            w.username = 'Fib'
            return [w]
        elif username == 'Bif':
            w.widget = "Widget2"
            w.username = 'Bif'
            return [w]


class APIKey:
    def __init__(self, name, key):
        self.name = name
        self.key = key


api_keys = {"GenericWidget": APIKey("APPID", "1234567890")}


class HtmlBuilderTest(unittest.TestCase):

    def setUp(self):
        self.resolver = WidgetResolver(api_keys=api_keys,
                                       widget_user_dao=WidgetUserDaoMock(), widget_dao=WidgetDaoMock())

    def test_without_api_key(self):
        resolved = self.resolver.process_widgets('Bif')
        self.assertEqual(url_mock, resolved[0].url)

    def test_with_api_key(self):
        resolved = self.resolver.process_widgets('Fib')
        self.assertEqual("www.example.com/rest&APPID=1234567890", resolved[0].url)

