from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from view import View, WebEngineFacade
import sys
from root_dir import ROOT_DIR
import time

index_html_path = ROOT_DIR + '/html/index.html'
index_html_test_path = ROOT_DIR + '/tests/test_data/test.html'

view = None


class ControllerMock(QRunnable):
    def __init__(self, view):
        super(ControllerMock, self).__init__()
        self.__view = view

    def run(self):
        time.sleep(3)
        self.__view.change_ui_mode()
        #view.load_index_html()  # need signal slot
        while True:
            pass



app = QApplication(sys.argv)

pool = QThreadPool()
view = View(False, WebEngineFacade.Standard, index_html_path)
c_mock = ControllerMock(view)
pool.start(c_mock)
view.show_window()

sys.exit(app.exec_())

# TODO:
# 1. Start main/ui thread
# 2. from main thread start controller thread
# 3. main thread should start executing ui