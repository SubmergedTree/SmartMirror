from api.rest import RestApi, RestApiSignal
from database.dao import UserDao, PictureDao, WidgetDao, WidgetUserDao
from recognition.camera import Camera, WhichCamera
from recognition.recognition import Scheduler
from widget.widget_resolver import WidgetResolver
from view.view import View, WebEngineFacade
from view.html_builder import HtmlBuilder
from load_config import ConfigLoader
from root_dir import ROOT_DIR

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot
import sys


class ConfigValues:
    Standard = WebEngineFacade.Standard
    Legacy = WebEngineFacade.Legacy
    Generic = WhichCamera.CV
    Pi = WhichCamera.PI


FRONTAL_FACE_PATH = '/util/lbpcascade_frontalface.xml'
CONFIG_PATH = '/config.json'

DEFAULT_WEB_ENGINE = ConfigValues.Standard
DEFAULT_CAMERA = ConfigValues.Generic
DEFAULT_SERVER_PORT = 5000
DEFAULT_MAPPING = {"standard": ConfigValues.Standard, "legacy": ConfigValues.Legacy,
                   "generic": ConfigValues.Generic, "pi": ConfigValues.Pi}

JS_DIR = ROOT_DIR + '/js'
HTML_DIR = ROOT_DIR + '/html'
HTML_INDEX = HTML_DIR + '/smart_mirror_index.html'


class Controller(QRunnable):
    def __init__(self,cascade_path, config, api_key_dict, view, thread_pool, RestServer, RecognizerScheduler, Camera, WidgetResolver,
                UserDao, PictureDao, WidgetDao, WidgetUserDao):
        super(Controller, self).__init__()
        self.__is_running = True
        self.__cascade_path = cascade_path
        self.__config = config
        self.__api_key_dict = api_key_dict
        self.__view = view
        self.__thread_pool = thread_pool

        self.__user_dao = UserDao()
        self.__picture_dao = PictureDao()
        self.__widget_dao = WidgetDao()
        self.__widget_user_dao = WidgetUserDao()

        self.__new_pictures_signal = RestApiSignal()
        self.__new_pictures_signal.new_pictures.connect(self.__new_pictures)

        #self.__rest_server = RestServer(self.__new_pictures_signal.new_pictures)

        self.__camera = Camera(self.__cascade_path, self.__config.camera)
        self.__recognizer_scheduler = RecognizerScheduler(self.__user_dao, self.__picture_dao,
                                                          self.__camera, self.__cascade_path, self.__is_learning_cb,
                                                          self.__finished_learning_cb, self.__user_recognized_callback)
        self.__widget_resolver = WidgetResolver(api_keys=self.__api_key_dict,
                                                widget_user_dao=self.__widget_user_dao, widget_dao=self.__widget_dao)

        #self.__thread_pool.start(self.__rest_server)

    def run(self): # For non blocking ui
        while self.__is_running:
            pass

    def shut_down(self):
        print("shut down")
        self.__recognizer_scheduler.shut_down()
        #try:
        #    self.__rest_server.shut_down()
        #except RuntimeError as e:
        #    print("error")
            # TODO: logging
        self.__is_running = False
        self.__thread_pool.waitForDone()

    def __is_learning_cb(self):
        print("is learning")

    def __finished_learning_cb(self):
        print("finished learning")

    def __user_recognized_callback(self, username):
        print("user recognized {}".format(username))

    def __new_pictures(self):
        print("new pictures")


def set_up():
    cascade = ROOT_DIR + FRONTAL_FACE_PATH
    config_loader = ConfigLoader(DEFAULT_WEB_ENGINE, DEFAULT_CAMERA, DEFAULT_SERVER_PORT, DEFAULT_MAPPING)
    api_key_dict, config = config_loader.load(CONFIG_PATH)
    mirror_app = QApplication(sys.argv)
    html_builder = HtmlBuilder(JS_DIR, HTML_DIR, HTML_INDEX)
    mirror_view = View(False, config.web_engine, html_builder.build_html())  # TODO FULLSCREEN
    return mirror_app, mirror_view, api_key_dict, config, cascade


if __name__ == '__main__':
    thread_pool = QThreadPool()
    app, view, api_key_dict, config, cascade = set_up()
    controller = Controller(cascade_path=cascade, config=config, api_key_dict=api_key_dict, view=view,
                            thread_pool=thread_pool, RestServer=RestApi,
                            RecognizerScheduler=Scheduler, Camera=Camera, WidgetResolver=WidgetResolver,
                            UserDao=UserDao, PictureDao=PictureDao, WidgetDao=WidgetDao, WidgetUserDao=WidgetUserDao)
    thread_pool.start(controller)
    app.aboutToQuit.connect(lambda: controller.shut_down())
    view.show_window()
    sys.exit(app.exec_())

