from api.rest import RestApi
from database.dao import UserDao, PictureDao, WidgetDao, WidgetUserDao
from recognition.camera import Camera
from recognition.recognition import Scheduler
from widget_controller import WidgetController
from view import View
from root_dir import ROOT_DIR

FRONTAL_FACE_PATH = "/util/lbpcascade_frontalface.xml"

# TODO must run in an seperate non main thread to avoid being blocked by View. View MUST run in main thread.
class Controller:
    def __init__(self, View, RestServer, RecognizerScheduler, Camera, WidgetController,UserDao, PictureDao, WidgetDao, WidgetUserDao):
        cascade = ROOT_DIR + FRONTAL_FACE_PATH

        self.__view = View()
        self.__rest_server = RestServer()
        self.__recognizer_scheduler = RecognizerScheduler()
        self.__camera = Camera()
        self.__widget_controller = WidgetController()
        self.__user_dao = UserDao()
        self.__picture_dao = PictureDao()
        self.__widget_dao = WidgetDao()
        self.__widget_user_dao = WidgetUserDao()

    def __is_learning_cb(self):
        pass

    def __finished_learning_cb(self):
        pass

    def __user_recognized_callback(self, username):
        pass

if __name__ == '__main__':
    controller = Controller(View=View, RestServer=RestApi, RecognizerScheduler=Scheduler,
                            Camera=Camera, WidgetController=WidgetController,UserDao=UserDao, PictureDao=PictureDao,
                            WidgetDao=WidgetDao, WidgetUserDao=WidgetUserDao)
