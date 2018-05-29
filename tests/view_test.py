from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from view import View, WebEngineFacade
import sys
from root_dir import ROOT_DIR

index_html_path = ROOT_DIR + 'index.html'
index_html_test_path = ROOT_DIR + 'tests/test_data/test.html'



class ControllerMock(QRunnable):
    def __int__(self):
        pass

    def run(self):
        while True:
            pass


c_mock = ControllerMock()

app = QApplication(sys.argv)
view = View(False, WebEngineFacade.Standard, index_html_test_path)
sys.exit(app.exec_())s

# TODO:
# 1. Start main/ui thread
# 2. from main thread start controller thread
# 3. main thread should start executing ui