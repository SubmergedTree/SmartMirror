# This Test should check the functionality of all ui/view related modules
from view.view import WebEngineFacade,View
from view.html_builder import HtmlBuilder
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time
from root_dir import ROOT_DIR


INDEX_HTML_PATH = ROOT_DIR + '/tests/integration_tests/test_data_view/html/smart_mirror_index.html'
WIDGET_JS_PATH = ROOT_DIR + '/tests/integration_tests/test_data_view/js'
WIDGET_HTML_PATH = ROOT_DIR + '/tests/integration_tests/test_data_view/html'

URL = 'http://api.icndb.com/jokes/random'
POSITION = 1
WIDGET_TYPE = 'ChuckNorisJoke'
CONTEXT = ''


class ControllerMock(QRunnable):
    def __init__(self, view):
        super(ControllerMock, self).__init__()
        self.__view = view

    def run(self):
        time.sleep(3)
        self.__view.load_widget(URL, POSITION, WIDGET_TYPE, CONTEXT)


app = QApplication([])
pool = QThreadPool()
html_builder = HtmlBuilder(WIDGET_JS_PATH, WIDGET_HTML_PATH, INDEX_HTML_PATH)
result = html_builder.build_html()
view = View(False, WebEngineFacade.Standard, result)
c_mock = ControllerMock(view)
pool.start(c_mock)
view.show_window()

sys.exit(app.exec_())