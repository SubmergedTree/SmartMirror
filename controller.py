from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from view import View
from api.rest import RestApi
from recognition.face_recognizer import FaceRecognizerScheduler


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
        self.__face_recognizer_scheduler = FaceRecognizerScheduler(self.__threadpool, self.__is_currently_learning, finished_learning_signal, recognized_user_signal)
        
    def __setup_signals(self):
        signals.new_picture.connect(self.new_picture)
        signals.recognized_user.connect(self.user_recognized)
        
    @pyqtSlot()
    def new_picture(self):   
        pass
    
    @pyqtSlot()
    def user_recognized(self, username):
        pass

    def __is_currently_learning(self):
        pass

    
controller = Controller(View(), RestApi(signals.new_picture))