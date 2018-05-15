from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

try:
    from PyQt5.QtWebKitWidgets import QWebView
except:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
import sys

from util import Logger

class WebEngine: # TODO: build wrapper to ensure compatibility with QWebView and QWebEngineView
    pass

class HtmlFileLocation():
    INDEX = 'index.html' 
    JOKE = 'joke.html'
    
    #we need html path, js path, widget name 
    # rest url is hardcoded in index.html
    
html = '''<b>Chuck Noris Jokes</b> <br> <br> <div id=\"jokeText\">'''    
js = '''function loadData(result) {
        document.getElementById('jokeText').innerHTML = result.value.joke;
}
fillWithData(http://api.icndb.com/jokes/random,loadData)
'''    

class View():
    def __init__(self, fullscreen):
        self.__win, self.__layout = self.__setup_window()
        self.__web_view = QWebView()
        self.__load_index_html("index.html")
        self.__frame = self.__setup_web_view()
        self.__layout.addWidget(self.__web_view)
        if fullscreen:
            self.__win.showFullScreen()
        self.__win.show()
        Logger.info('View is ready.')
        
    def __setup_window(self):
        window = QWidget()
        window.setWindowTitle('SmartMirror')
        layout = QVBoxLayout()
        window.setLayout(layout)
        return window, layout
    
    
    def __load_index_html(self, path):
        html = ''
        with open(path, 'r') as fh:
            html = fh.read()
            Logger.info('HTML Source: ' + path)
        self.__web_view.setHtml(html)  
    
    
    def load_widget_html(self, widget_name):
        pass    
        
    def __setup_web_view(self):
        return self.__web_view.page().mainFrame()      
    
    
    def change_ui_mode(self):
        self.__frame.evaluateJavaScript('changeMode();')
    
    
    def change_widget(self, position):
        self.__frame.evaluateJavaScript('changeWidget('+ str(position) +','+ '<b>Chuck Noris Jokes</b> <br> <br> <div id=\"jokeText\">' +');')
    
     
    def fill_with_data(self):
        #self.__frame.evaluateJavaScript('fillWithData();')
        pass

    
    def reset_widgets(self):
        self.__frame.evaluateJavaScript(js)
        
app = QApplication([])

main_view = View(False)
 
sys.exit(app.exec_())


        