from datetime import datetime
from util.logger import Logger


class HttpStatus:
    SUCCESS = 200
    CREATED = 201
    BADREQUEST = 400
    FORBIDDEN = 403
    NOTFOUND = 404
    CONFLICT = 409
    INTERNALSERVERERROR = 500


INTERNAL_SERVER_ERROR_MSG = '500 - Internal Server Error'


class RestBroker:
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        self.get_users = GetUsers(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
        self.new_user = NewUser(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
        self.delete_user = DeleteUser(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
        self.add_picture = AddPictures(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)
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
        Logger.info('request: getUsers.')
        try:
            user_list = self._UserDao.get_all_user()
            return user_list, HttpStatus.SUCCESS
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class NewUser(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(NewUser, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self, username, prename, name):
        try:
            res = self._UserDao.insert_user(username, prename, name)
            return ('New User created', HttpStatus.CREATED) if res else ('User already exists', HttpStatus.CONFLICT)
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class DeleteUser(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(DeleteUser, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self, username):
        try:
            res = self._UserDao.delete_user_by_username(username)
            return ('User successfully deleted', HttpStatus.SUCCESS) if res else ('User not found', HttpStatus.NOTFOUND)
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class AddPictures(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(AddPictures, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self, username, pictures):
        for picture in pictures:
            image_name = username + str(datetime.now()) # TODO


class GetWidgets(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(GetWidgets, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self):
        try:
            return self._WidgetDao.get_widgets(), HttpStatus.SUCCESS
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class UpdateWidgetOfPerson(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(UpdateWidgetOfPerson, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self, username, widget, position, context):
        try:
            self._WidgetUserDao.update(widget, username, position, context)
            return 'Widget Updated', HttpStatus.SUCCESS
        except self._DBException:
            return INTERNAL_SERVER_ERROR_MSG, HttpStatus.INTERNALSERVERERROR


class NewWidget(RestImplBase):
    def __init__(self, UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException):
        super(NewWidget, self).__init__(UserDao, PictureDao, WidgetDao, WidgetUserDao, DBException)

    def __call__(self, widget, base_url):
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
        return True  # TODO (object which stores state)
