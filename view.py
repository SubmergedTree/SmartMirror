import PyQt5
from PyQt5.QtCore import QUrl 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton 
from PyQt5.QtWebKitWidgets import QWebView , QWebPage
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtNetwork import *
import sys

class View():
    def __init__(self):
        self.__win, self.__layout = self.__setup_window()
        self.__web_view = QWebView()
        self.__load_html("index.html")
        self.__layout.addWidget(self.__web_view)
        self.__win.show()
        
    def __setup_window(self):
        window = QWidget()
        window.setWindowTitle('SmartMirror')
        layout = QVBoxLayout()
        window.setLayout(layout)
        return window, layout
    
    def __load_html(self, path):
        html = ''
        css = ''
        with open(path, 'r') as fh:
            html = fh.read()
        self.__web_view.setHtml(html)    
        
        
app = QApplication([])

main_view = View()

              
app.exec_() 
        