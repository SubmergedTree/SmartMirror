from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from view import View, WebEngineFacade
import sys
from root_dir import ROOT_DIR

index_html_path = ROOT_DIR + 'index.html'

app = QApplication(sys.argv)
view = View(False, WebEngineFacade.Standard)
sys.exit(app.exec_())


# TODO:
# 1. Start main/ui thread
# 2. from main thread start controller thread
# 3. main thread should start executing ui