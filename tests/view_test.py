from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from view import View, WebEngineFacade
import sys
from root_dir import ROOT_DIR

index_html_path = ROOT_DIR + 'index.html'
index_html_test_path = ROOT_DIR + '/tests/test_data/test.html'

view = None

class ControllerMock(QRunnable):
    def __int__(self):
        pass

    def run(self):
        view.load_index_html()  # need signal slot
        while True:
            pass



app = QApplication(sys.argv)

c_mock = ControllerMock()
pool = QThreadPool()
view = View(False, WebEngineFacade.Standard, index_html_test_path)
pool.start(c_mock)
view.show_window()

sys.exit(app.exec_())

# TODO:
# 1. Start main/ui thread
# 2. from main thread start controller thread
# 3. main thread should start executing ui