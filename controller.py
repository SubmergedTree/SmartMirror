from api.rest import RestApi
from api.rest_impl import RestBroker, RestImplSignal
from database.dao import UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException
from recognition.camera import Camera, WhichCamera
from recognition.recognition import Scheduler
from widget.widget_resolver import WidgetResolver
from view.view import View, WebEngineFacade
from view.html_builder import HtmlBuilder
from load_config import ConfigLoader
from root_dir import ROOT_DIR

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThreadPool, QRunnable, QTimer
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

WIDGET_SHOW_TIME = 300  # TODO make configurable

JS_DIR = ROOT_DIR + '/js'
HTML_DIR = ROOT_DIR + '/html'
HTML_INDEX = HTML_DIR + '/smart_mirror_index.html'
IMAGE_BASE_PATH = ''


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

        self.rest_impl_signals = RestImplSignal()
        self.rest_impl_signals.new_pictures.connect(self.__relearn)
        self.rest_impl_signals.users_changed.connect(self.__relearn)

        self.__rest_server = RestServer(RestBroker(user_dao=self.__user_dao, picture_dao=self.__picture_dao,
                                                   widget_dao=self.__widget_dao,
                                                   widget_user_dao=self.__widget_user_dao, DBException=DBException,
                                                   new_pictures_signal=self.rest_impl_signals.new_pictures,
                                                   users_changed_signal=self.rest_impl_signals.users_changed,
                                                   image_base_path=IMAGE_BASE_PATH), DEFAULT_SERVER_PORT)

        self.__camera = Camera(self.__cascade_path, self.__config.camera)
        self.__recognizer_scheduler = RecognizerScheduler(self.__user_dao, self.__picture_dao,
                                                          self.__camera, self.__cascade_path, self.__is_learning_cb,
                                                          self.__finished_learning_cb,self.__no_training_data_cb,
                                                          self.__user_recognized_callback,
                                                          self.__learning_error_cb)
        self.__widget_resolver = WidgetResolver(api_keys=self.__api_key_dict,
                                                widget_user_dao=self.__widget_user_dao, widget_dao=self.__widget_dao)

        self.__show_widgte_finished_timer = None

        self.__rest_server.start()

    def run(self): # For non blocking ui
        while self.__is_running:
            pass

    def shut_down(self):
        print("shut down")
        self.__recognizer_scheduler.shut_down()
        self.__rest_server.shut_down()
        self.__is_running = False
        self.__thread_pool.waitForDone()

    def __is_learning_cb(self):
        print("is learning") # TODO view shows hint

    def __finished_learning_cb(self):
        print("finished learning") # TODO remove learning hint

    def __no_training_data_cb(self):
        print("no training data")

    def __user_recognized_callback(self, username):
        print("user recognized {}".format(username))
        self.__view.change_ui_mode()
        widgets = self.__widget_resolver.process_widgets(username)
        for widget in widgets:
            self.__view.load_widget(widget.url, widget.position, widget.widget, widget.context)
        self.__show_widgte_finished_timer = QTimer()
        self.__show_widgte_finished_timer.timeout.connect(self.__on_show_widget_finished)
        self.__show_widgte_finished_timer.setSingleShot(True)
        self.__show_widgte_finished_timer.start(WIDGET_SHOW_TIME)

    def __on_show_widget_finished(self):
        print("on widget finished")
        self.__view.reset_widgets()
        self.__view.change_ui_mode()
        self.__recognizer_scheduler.schedule()

    def __relearn(self):
        print("relearn")
        self.__recognizer_scheduler.learn()

    def __learning_error_cb(self):
        pass


def set_up():
    cascade = ROOT_DIR + FRONTAL_FACE_PATH
    config_loader = ConfigLoader(DEFAULT_WEB_ENGINE, DEFAULT_CAMERA, DEFAULT_SERVER_PORT, DEFAULT_MAPPING)
    api_key_dict, config = config_loader.load(CONFIG_PATH)
    mirror_app = QApplication(sys.argv)
    html_builder = HtmlBuilder(JS_DIR, HTML_DIR, HTML_INDEX)
    mirror_view = View(False, config.web_engine, html_builder.build_html())  # TODO FULLSCREEN
    return mirror_app, mirror_view, api_key_dict, config, cascade


if __name__ == '__main__':
    thread_pool = QThreadPool() # TODO use single thread with moveToThread instead of threadpool
    app, mirror_view, api_key_dict, config, cascade = set_up()
    controller = Controller(cascade_path=cascade, config=config, api_key_dict=api_key_dict, view=mirror_view,
                            thread_pool=thread_pool, RestServer=RestApi,
                            RecognizerScheduler=Scheduler, Camera=Camera, WidgetResolver=WidgetResolver,
                            UserDao=UserDao, PictureDao=PictureDao, WidgetDao=WidgetDao, WidgetUserDao=WidgetUserDao)
    thread_pool.start(controller)
    app.aboutToQuit.connect(lambda: controller.shut_down())
    mirror_view.show_window()
    sys.exit(app.exec_())

