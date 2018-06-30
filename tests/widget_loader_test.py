import unittest
from loader.load_widgets import WidgetLoader
from loader.load_urls import UrlMapping


class WidgetDaoMock:
    def __init__(self, mapping):
        self.mapping = mapping

    def add_widget(self, widget, base_url):
        self.mapping[widget] = base_url

    def delete_widget(self, widget):
        self.mapping.pop(widget)

    def get_widgets(self):
        widgets = []
        for widget, url in self.mapping.items():
            widgets.append(widget)
        return widgets


class TestWidgetLoader(unittest.TestCase):

    def test_add_widget(self):
        url_mapping_in_db = {'foo': 'fooUrl'}
        widget_dao_mock = WidgetDaoMock(url_mapping_in_db)
        new_url_mapping = [UrlMapping('bar', 'barUrl'), UrlMapping('foo', 'fooUrl')]
        widget_loader = WidgetLoader(widget_dao_mock, new_url_mapping)
        widget_loader.update_widget_table()
        self.assertEqual({'foo':'fooUrl', 'bar':'barUrl'}, widget_dao_mock.mapping)

    def test_delete_widget(self):
        url_mapping_in_db = {'foo':'fooUrl', 'bar':'barUrl'}
        widget_dao_mock = WidgetDaoMock(url_mapping_in_db)
        new_url_mapping = [UrlMapping('bar', 'barUrl')]
        widget_loader = WidgetLoader(widget_dao_mock, new_url_mapping)
        widget_loader.update_widget_table()
        self.assertEqual({'bar':'barUrl'}, widget_dao_mock.mapping)

    def test_add_and_delete_widget(self):
        url_mapping_in_db = {'foo':'fooUrl', 'bar':'barUrl'}
        widget_dao_mock = WidgetDaoMock(url_mapping_in_db)
        new_url_mapping = [UrlMapping('bar', 'barUrl'), UrlMapping('baz', 'bazUrl')]
        widget_loader = WidgetLoader(widget_dao_mock, new_url_mapping)
        widget_loader.update_widget_table()
        self.assertEqual({'bar':'barUrl', 'baz': 'bazUrl'}, widget_dao_mock.mapping)
