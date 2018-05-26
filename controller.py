from api.rest import RestApi
from database.dao import UserDao, PictureDao, WidgetDao, WidgetUserDao
from recognition.camera import Camera
from recognition.recognition import Scheduler
from view import View
from root_dir import ROOT_DIR


class Controller:
    def __init__(self, View, RestServer, RecognizerScheduler, Camera, UserDao, PictureDao, WidgetDao, WidgetUserDao):
        cascade = ROOT_DIR + "/util/lbpcascade_frontalface.xml"

        self.__view = View()
        self.__rest_server = RestServer()
        self.__recognizer_scheduler = RecognizerScheduler()
        self.__camera = Camera()
        self.__user_dao = UserDao()
        self.__picture_dao = PictureDao()
        self.__widget_dao = WidgetDao()
        self.__widget_user_dao = WidgetUserDao()



if __name__ == '__main__':
    controller = Controller(View=View, RestServer=RestApi, RecognizerScheduler=Scheduler,
                            Camera=Camera, UserDao=UserDao, PictureDao=PictureDao,
                            WidgetDao=WidgetDao, WidgetUserDao=WidgetUserDao)
