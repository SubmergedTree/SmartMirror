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
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException, new_pictures_signal,
                 users_changed_signal, image_base_path):
        self.get_users = GetUsers(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)
        self.delete_user = DeleteUser(user_dao, picture_dao, widget_dao, widget_user_dao, DBException, users_changed_signal)
        self.add_picture = AddPictures(user_dao, picture_dao, widget_dao, widget_user_dao, DBException,
                                       new_pictures_signal, image_base_path)
        self.get_widgets = GetWidgets(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)
        self.update_widget_of_person = UpdateWidgetOfPerson(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)
        self.new_widget = NewWidget(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)
        self.status = Status(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)
        self.new_user = NewUser(user_dao, picture_dao, widget_dao, widget_user_dao, DBException, self.add_picture, users_changed_signal)
        self.delete_widget = DeleteWidget(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)


class RestImplBase:
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException):
        self._user_dao = user_dao
        self._picture_dao = picture_dao
        self._widget_dao = widget_dao
        self._widget_user_dao = widget_user_dao
        self._DBException = DBException


class GetUsers(RestImplBase):
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException):
        super(GetUsers, self).__init__(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)

    def __call__(self):
        Logger.info('request: getUsers')
        try:
            user_list = self._user_dao.get_all_user()
            user_list_serializable = []
            for user in user_list:
                user_list_serializable.append({'username': user.username,
                                               'prename': user.prename,
                                               'name': user.prename})
            return user_list_serializable, HttpStatus.SUCCESS
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class NewUser(RestImplBase):
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException, add_picture,users_changed_signal):
        super(NewUser, self).__init__(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)
        self.__users_changed_signal = users_changed_signal
        self.__add_picture = add_picture

    def __call__(self, username, prename, name, image, save_func):
        Logger.info('request: newUser; username: {}'.format(username))
        try:
            res = self._user_dao.insert_user(username, prename, name)
            if not res:
                return 'User already exists', HttpStatus.CONFLICT
            result, status = self.__add_picture(username, [image], save_func)
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
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException, users_changed_signal):
        super(DeleteUser, self).__init__(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)
        self.__users_changed_signal = users_changed_signal

    def __call__(self, username):
        Logger.info('request: deleteUser; username: {}'.format(username))
        try:
            res = self._user_dao.delete_user_by_username(username)
            self.__users_changed_signal.emit()
            return ('User successfully deleted', HttpStatus.SUCCESS) if res else ('User not found', HttpStatus.NOTFOUND)
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class AddPictures(RestImplBase):
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException, new_pictures_signal, image_base_path):
        super(AddPictures, self).__init__(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)
        self.__new_pictures_signal = new_pictures_signal
        self.__image_base_path = image_base_path

    def __call__(self, username, pictures, save_func): # TODO PATH
        Logger.info('request: addPictures; username: {}'.format(username))
        try:
            if self._user_dao.get_user_by_username(username):
                for picture in pictures:
                    image_path = username + str(datetime.now())
                    path = save_func(picture, self.__image_base_path, image_path)
                    if not self._picture_dao.add_picture(username, path):
                        Logger.warn("Failed to add new paths to database. User: {}".format(username))
                        return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR
                self.__new_pictures_signal.emit()
                return "Pictures successfully added", HttpStatus.SUCCESS
            else:
                return "User {} does not exist".format(username), HttpStatus.NOTFOUND
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class GetWidgets(RestImplBase):
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException):
        super(GetWidgets, self).__init__(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)

    def __call__(self):
        Logger.info('request: getWidgets')
        try:
            widgets = self._widget_dao.get_widgets()
            widget_list_serializable = []
            for widget in widgets:
                widget_list_serializable.append({'widget': widget.widget,
                                                 'base_url': widget.base_url})
            return widget_list_serializable, HttpStatus.SUCCESS
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class UpdateWidgetOfPerson(RestImplBase):
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException):
        super(UpdateWidgetOfPerson, self).__init__(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)

    def __call__(self, username, widget, position, context):
        Logger.info('request: updateWidgetsOfPerson; username: {}; widget: {}'.format(username, widget))
        if not context or context == '':
            context = 'None'
        try:
            result = self._widget_user_dao.update(widget, username, position, context)
            if result:
                return 'Widget Updated', HttpStatus.SUCCESS
            else:
                return 'Widget Updated', HttpStatus.CONFLICT
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class NewWidget(RestImplBase):
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException):
        super(NewWidget, self).__init__(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)

    def __call__(self, widget, base_url):
        Logger.info('request: newWidget; widget: {}; base_url: {}'.format(widget, base_url))
        try:
            res = self._widget_dao.add_widget(widget, base_url)
            return ('Widget Created', HttpStatus.CREATED) if res else ('Widget already exists', HttpStatus.CONFLICT)
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class DeleteWidget(RestImplBase):
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException):
        super(DeleteWidget, self).__init__(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)

    def __call__(self, widget):
        Logger.info('request: deleteWidget; widget: {}'.format(widget))
        try:
            res = self._widget_dao.delete_widget(widget)
            return ('Widget successfully deleted', HttpStatus.SUCCESS) if res else ('Widget not found', HttpStatus.NOTFOUND)
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


# TODO reset


class Status(RestImplBase):
    def __init__(self, user_dao, picture_dao, widget_dao, widget_user_dao, DBException):
        super(Status, self).__init__(user_dao, picture_dao, widget_dao, widget_user_dao, DBException)

    def __call__(self):
        Logger.info('request: status; username')
        return {"status:" "up"}  # TODO (object which stores state)
