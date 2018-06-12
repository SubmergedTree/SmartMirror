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


#class ViewSignals:
#    pass

class View:
    def __init__(self, fullscreen, which_web_engine, index_html):
        self.__index_html = index_html
        self.__win, self.__layout = self.__setup_window()
        self.__web_engine = WebEngineFacade(which_web_engine, self.__layout)

    def __setup_window(self):
        window = QWidget()
        window.setWindowTitle('SmartMirror')
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

    def change_ui_mode(self):
        self.__web_engine.engine.eval_js('changeMode();')

    def reset_widgets(self):
        self.__web_engine.engine.eval_js('resetWidgets();')

    def load_widget(self, url, position, widget_type, context):
        js = 'loadWidget(\'{}\', \'{}\', \'{}\', \'{}\');'.format(url, position, widget_type, context)
        self.__web_engine.engine.eval_js(js)


# class HtmlFileLocation():
#     INDEX = 'index.html'
#     JOKE = 'joke.html'
#
#     #we need html path, js path, widget name
#     # rest url is hardcoded in index.html        self.__web_engine.engine.eval_js('changeMode();')
#
# html = '''<b>Chuck Noris Jokes</b> <br> <br> <div id=\"jokeText\">'''
# js = '''function loadData(result) {
#         document.getElementById('jokeText').innerHTML = result.value.joke;
# }
# fillWithData(http://api.icndb.com/jokes/random,loadData)
# '''
#
# class View:
#     def __init__(self, fullscreen):
#         self.__win, self.__layout = self.__setup_window()
#         self.__web_view = QWebView()
#         self.__load_index_html("index.html")
#         self.__frame = self.__setup_web_view()
#         self.__layout.addWidget(self.__web_view)
#         if fullscreen:
#             self.__win.showFullScreen()
#         self.__win.show()
#         Logger.info('View is ready.')
#
#     def __setup_window(self):
#         window = QWidget()
#         window.setWindowTitle('SmartMirror')
#         layout = QVBoxLayout()
#         window.setLayout(layout)
#         return window, layout
#
#
#     def __load_index_html(self, path):
#         html = ''
#         with open(path, 'r') as fh:
#             html = fh.read()
#             Logger.info('HTML Source: ' + path)
#         self.__web_view.setHtml(html)
#
#
#     def load_widget_html(self, widget_name):
#         pass
#
#     def __setup_web_view(self):
#         return self.__web_view.page().mainFrame()
#
#
#     def change_ui_mode(self):
#         self.__frame.evaluateJavaScript('changeMode();')
#
#
#     def change_widget(self, position):
#         self.__frame.evaluateJavaScript('changeWidget('+ str(position) +','+ '<b>Chuck Noris Jokes</b> <br> <br> <div id=\"jokeText\">' +');')
#
#
#     def fill_with_data(self):
#         #self.__frame.evaluateJavaScript('fillWithData();')
#         pass
#
#
#     def reset_widgets(self):
#         self.__frame.evaluateJavaScript(js)
#
# app = QApplication([])
#
# main_view = View(False)
#
# sys.exit(app.exec_())
