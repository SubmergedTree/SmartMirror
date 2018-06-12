from api.rest import RestApi
from database.dao import UserDao, PictureDao, WidgetDao, WidgetUserDao
from recognition.camera import Camera
from recognition.recognition import Scheduler
from widget.widget_resolver import WidgetResolver
from view.view import View
from view.html_builder import HtmlBuilder
from load_config import ConfigLoader
from root_dir import ROOT_DIR


class ConfigValues:
    Standard = "standard"
    Legacy = "legacy"
    Generic = "generic"
    Pi = "pi"


FRONTAL_FACE_PATH = '/util/lbpcascade_frontalface.xml'
CONFIG_PATH = '/config.json'

DEFAULT_WEB_ENGINE = ConfigValues.Standard
DEFAULT_CAMERA = ConfigValues.Generic
DEFAULT_SERVER_PORT = 5000
DEFAULT_MAPPING = {"standard": ConfigValues.Standard, "legacy": ConfigValues.Legacy,
                   "generic":ConfigValues.Generic, "pi": ConfigValues.Pi}

JS_DIR = ROOT_DIR + '/js'
HTML_DIR = ROOT_DIR + '/html'
HTML_INDEX = ROOT_DIR + HTML_DIR + '/smart_mirror_index.html'

# TODO must run in an seperate non main thread to avoid being blocked by View. View MUST run in main thread.
class Controller:
    def __init__(self, View, RestServer, RecognizerScheduler, Camera, WidgetResolver, HTMLBuilder,
                 ConfigLoader ,UserDao, PictureDao, WidgetDao, WidgetUserDao):
        self.__WidgetResolver = WidgetResolver
        cascade = ROOT_DIR + FRONTAL_FACE_PATH

        self.__config_Loader = ConfigLoader(DEFAULT_WEB_ENGINE, DEFAULT_CAMERA, DEFAULT_SERVER_PORT, DEFAULT_MAPPING)
        self.__html_builder = HTMLBuilder(JS_DIR, HTML_DIR, HTML_INDEX)

        self.__user_dao = UserDao()
        self.__picture_dao = PictureDao()
        self.__widget_dao = WidgetDao()
        self.__widget_user_dao = WidgetUserDao()

        self.__set_up()

        self.__view = View()
        self.__rest_server = RestServer()
        self.__recognizer_scheduler = RecognizerScheduler()
        self.__camera = Camera()
        self.__widget_resolver = WidgetResolver()
        self.__html_builder = HTMLBuilder()

    def __set_up(self):
        api_key_dict, config = self.__config_Loader.load(CONFIG_PATH)
        self.__widget_resolver = self.__WidgetResolver(api_key_dict, self.__widget_user_dao, self.__widget_dao)
        self.__view = View(False, config.web_engine, self.__html_builder.build())  # TODO FULLSCREEN

    def __restart(self):
        pass

    def __is_learning_cb(self):
        pass

    def __finished_learning_cb(self):
        pass

    def __user_recognized_callback(self, username):
        pass


if __name__ == '__main__':
    controller = Controller(View=View, RestServer=RestApi, RecognizerScheduler=Scheduler,
                            Camera=Camera, WidgetResolver=WidgetResolver,HTMLBuilder=HtmlBuilder,
                            ConfigLoader=ConfigLoader, UserDao=UserDao, PictureDao=PictureDao,
                            WidgetDao=WidgetDao, WidgetUserDao=WidgetUserDao)
