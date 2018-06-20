from datetime import datetime
from util.logger import Logger
from PyQt5.QtCore import pyqtSignal, QObject


class RestImplSignal(QObject):
    new_pictures = pyqtSignal()
    users_changed = pyqtSignal()


class HttpStatus:
    SUCCESS = 200
    CREATED = 201
    BADREQUEST = 400
    FORBIDDEN = 403
    NOTFOUND = 404
    CONFLICT = 409
    INTERNALSERVERERROR = 500


INTERNAL_SERVER_ERROR_MSG = '500 - Internal Server Error'

# TODO write daos in lower case
class RestBroker:
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException, new_pictures_signal, users_changed_signal,image_base_path):
        self.get_users = GetUsers(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
        self.new_user = NewUser(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException, users_changed_signal)
        self.delete_user = DeleteUser(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException, users_changed_signal)
        self.add_picture = AddPictures(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException,
                                       new_pictures_signal, image_base_path)
        self.get_widgets = GetWidgets(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
        self.update_widget_of_person = UpdateWidgetOfPerson(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
        self.new_widget = NewWidget(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
        self.status = Status(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)


class RestImplBase:
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        self._UserDao = UserDao
        self._PictureDao = PictureDao
        self._WidgetDao = WidgetDao
        self._WidgetUserDao = WidgetUserDao
        self._DBException = DBException


class GetUsers(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(GetUsers, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self):
        Logger.info('request: getUsers')
        try:
            user_list = self._UserDao.get_all_user()
            user_list_serializable = []
            for user in user_list:
                user_list_serializable.append({'username': user.username,
                                               'prename': user.prename,
                                               'name': user.prename})
            return user_list_serializable, HttpStatus.SUCCESS
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class NewUser(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException, users_changed_signal):
        super(NewUser, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
        self.__users_changed_signal = users_changed_signal

    def __call__(self, username, prename, name, image, save_func):
        Logger.info('request: newUser; username: {}'.format(username))
        try:
            res = self._UserDao.insert_user(username, prename, name)
            if not res:
                return 'User already exists', HttpStatus.CONFLICT
            result, status = self._PictureDao.add_picture(username, [image], save_func)
            if status == HttpStatus.NOTFOUND:
                return 'Could not save image, user not found', HttpStatus.NOTFOUND
            elif status == HttpStatus.INTERNALSERVERERROR:
                return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR
            else:
                self.__users_changed_signal.emit()
                return ('New User created', HttpStatus.CREATED)
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class DeleteUser(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException, users_changed_signal):
        super(DeleteUser, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
        self.__users_changed_signal = users_changed_signal

    def __call__(self, username):
        Logger.info('request: deleteUser; username: {}'.format(username))
        try:
            res = self._UserDao.delete_user_by_username(username)
            self.__users_changed_signal.emit()
            return ('User successfully deleted', HttpStatus.SUCCESS) if res else ('User not found', HttpStatus.NOTFOUND)
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class AddPictures(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException, new_pictures_signal, image_base_path):
        super(AddPictures, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
        self.__new_pictures_signal = new_pictures_signal
        self.__image_base_path = image_base_path

    def __call__(self, username, pictures, save_func): # TODO PATH
        Logger.info('request: addPictures; username: {}'.format(username))
        try:
            if self._UserDao.get_user_by_username(username):
                for picture in pictures:
                    image_path = username + str(datetime.now())
                    self._PictureDao.add_picture(username, image_path)
                    save_func(picture, image_path)
                self.__new_pictures_signal.emit()
                return "Pictures successfully added", HttpStatus.SUCCESS
            else:
                return "User {} does not exist".format(username), HttpStatus.NOTFOUND
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class GetWidgets(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(GetWidgets, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self):
        Logger.info('request: getWidgets')
        try:
            widgets = self._WidgetDao.get_widgets()
            widget_list_serializable = []
            for widget in widgets:
                widget_list_serializable.append({'widget': widget.username,
                                                 'base_url': widget.base_url})
            return widget_list_serializable, HttpStatus.SUCCESS
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class UpdateWidgetOfPerson(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(UpdateWidgetOfPerson, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self, username, widget, position, context):
        Logger.info('request: updateWidgetsOfPerson; username: {}; widget: {}'.format(username, widget))
        try:
            self._WidgetUserDao.update(widget, username, position, context)
            return 'Widget Updated', HttpStatus.SUCCESS
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class NewWidget(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(NewWidget, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self, widget, base_url):
        Logger.info('request: newWidget; widget: {}; base_url: {}'.format(widget, base_url))
        try:
            res = self._WidgetDao.add_widget(widget, base_url)
            return ('Widget Created', HttpStatus.CREATED) if res else ('Widget already exists', HttpStatus.CONFLICT)
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


# TODO delete widgets; reset


class Status(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(Status, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self):
        Logger.info('request: status; username')
        return True  # TODO (object which stores state)
