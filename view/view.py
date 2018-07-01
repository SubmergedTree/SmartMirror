from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
import sys
from util.logger import Logger

try:
    from PyQt5.QtWebKitWidgets import QWebView
    has_imported_legacy = True
except:
    has_imported_legacy = False

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    has_imported_standard = True
except:
    has_imported_standard = False


class CouldNotImportException(Exception):
    def __init__(self, message):
        super(CouldNotImportException, self).__init__(message)


class WebEngineLegacy:
    def __init__(self, layout):
        self.__web_view = QWebView()
        layout.addWidget(self.__web_view)

    def load_html(self, html):
        self.__web_view.setHtml(html)

    def eval_js(self, js):
        self.__web_view.page().mainFrame().evaluateJavaScript(js)


class WebEngineStandard:
    def __init__(self, layout):
        self.__web_view = QWebEngineView()
        layout.addWidget(self.__web_view)

    def load_html(self, html):
        self.__web_view.setHtml(html)

    def eval_js(self, js):
        self.__web_view.page().runJavaScript(js)


class WebEngineFacade:
    Legacy = 0
    Standard = 1

    def __init__(self, which, layout):
        if which == WebEngineFacade.Legacy:
            if not has_imported_legacy:
                raise CouldNotImportException("Could not import Legacy Web Engine: QtWebKitWidgets")
            self.__engine = WebEngineLegacy(layout)
        elif which == WebEngineFacade.Standard:
            if not has_imported_standard:
                raise CouldNotImportException("Could not import Standard Web Engine: QWebEngineView")
            self.__engine = WebEngineStandard(layout)

    @property
    def engine(self):
        return self.__engine


class View:
    def __init__(self, fullscreen, which_web_engine, index_html):
        self.__index_html = index_html
        self.__win, self.__layout = self.__setup_window(fullscreen)
        try:
            self.__web_engine = WebEngineFacade(which_web_engine, self.__layout)
        except CouldNotImportException as e:
            Logger.error('Could not import chosen web engine')
            raise e

    def __setup_window(self, fullscreen):
        window = QWidget()
        window.setWindowTitle('SmartMirror')
        if fullscreen:
            window.showFullScreen()
        layout = QVBoxLayout()
        window.setLayout(layout)
        return window, layout

    def __load_index_html(self):
        # with open(self.__index_html_path) as fh:
            # html = fh.read()
        self.__web_engine.engine.load_html(self.__index_html)

    def show_window(self):
        self.__win.show()
        self.__load_index_html()

    #def change_ui_mode(self):
    #    self.__web_engine.engine.eval_js('changeMode();')

    def change_mode_to_show_widgets(self):
        self.__web_engine.engine.eval_js('changeModeToWidgets();')

    def change_mode_to_idle(self):
        self.__web_engine.engine.eval_js('changeModeToIdle();')

    def change_mode_to_learning(self):
        self.__web_engine.engine.eval_js('changeModeToLearning();')

    def reset_widgets(self):
        self.__web_engine.engine.eval_js('resetWidgets();')

    def load_widget(self, url, position, widget_type, context):
        js = 'loadWidget(\'{}\', \'{}\', \'{}\', \'{}\');'.format(url, position, widget_type, context)
        self.__web_engine.engine.eval_js(js)

