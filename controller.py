from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from view import View
from rest import RestApi
from face_recognizer import Learner, Recognizer


class Signals(QObject):
    new_picture = pyqtSignal()
    finished_learning = pyqtSignal(list, object)
    recognized_user = pyqtSignal(str)

signals = Signals()
   

class Controller():
    def __init__(self, view, api):
        self.__app = QApplication(sys.argv, rest)
        self.__view = view
        self.__api = api
        self.__threadpool = QThreadPool()
        
    def __setup_signals(self):
        signals.new_picture.connect(new_picture)  
        signals.recognized_user.connect(user_recognized) 
        
    @pyqtSlot()
    def new_picture(self):   
        pass
    
    @pyqtSlot()
    def user_recognized(self, username):
        pass   

    
controller = Controller(View(), RestApi(signals.new_picture))   
        
        