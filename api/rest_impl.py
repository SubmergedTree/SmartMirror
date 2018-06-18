from datetime import datetime


class RestBroker:
    def __init__(self, SafeSession, User, Picture, Widget, WidgetUser):
        self.get_users = GetUsers(SafeSession, User, Picture, Widget, WidgetUser)
        self.new_user = NewUser(SafeSession, User, Picture, Widget, WidgetUser)
        self.delete_user = DeleteUser(SafeSession, User, Picture, Widget, WidgetUser)
        self.add_picture = AddPictures(SafeSession, User, Picture, Widget, WidgetUser)
        self.get_widgets = GetWidgets(SafeSession, User, Picture, Widget, WidgetUser)
        self.update_widget_of_person = UpdateWidgetOfPerson(SafeSession, User, Picture, Widget, WidgetUser)
        self.new_widget = NewWidget(SafeSession, User, Picture, Widget, WidgetUser)
        self.status = Status(SafeSession, User, Picture, Widget, WidgetUser)


class RestImplBase:
    def __init__(self, SafeSession, User, Picture, Widget, WidgetUser):
        self._SafeSession = SafeSession
        self._User = User
        self._Picture = Picture
        self._Widget = Widget
        self._WidgetUser = WidgetUser


class GetUsers(RestImplBase):
    def __init__(self, SafeSession, User, Picture, Widget, WidgetUser):
        super(GetUsers, self).__init__(SafeSession, User, Picture, Widget, WidgetUser)

    def __call__(self):
        user_list = []
        with self._SafeSession() as safe_session:
            for user in safe_session.get_session().query(self._User):
                user_dict = {'username': user.username,
                             'prename': user.prename,
                             'name': user.name}
                user_list.append(user_dict)
        return user_list


class NewUser(RestImplBase):
    def __init__(self, SafeSession, User, Picture, Widget, WidgetUser):
        super(NewUser, self).__init__(SafeSession, User, Picture, Widget, WidgetUser)

    def __call__(self, username, prename, name):
        with self._SafeSession() as safe_session:
            if safe_session.get_session().query(self._User).filter_by(username=username).first() is None:
                user = self._User(username=username, prename=prename, name=name)
                safe_session.add(user)
                safe_session.commit()
                return True
            else:
                return False


class DeleteUser(RestImplBase):
    def __init__(self, SafeSession, User, Picture, Widget, WidgetUser):
        super(DeleteUser, self).__init__(SafeSession, User, Picture, Widget, WidgetUser)

    def __call__(self, username):
        with self._SafeSession() as safe_session:
            user_to_delete = safe_session.get_session().query(self._User).filter_by(username=username).first()
            if user_to_delete:
                safe_session.delete(user_to_delete)
                safe_session.commit()
                return True
            else:
                return False


class AddPictures(RestImplBase):
    def __init__(self, SafeSession, User, Picture, Widget, WidgetUser):
        super(AddPictures, self).__init__(SafeSession, User, Picture, Widget, WidgetUser)

    def __call__(self, username, pictures):
        for picture in pictures:
            image_name = username + str(datetime.now()) # TODO


class GetWidgets(RestImplBase):
    def __init__(self, SafeSession, User, Picture, Widget, WidgetUser):
        super(GetWidgets, self).__init__(SafeSession, User, Picture, Widget, WidgetUser)

    def __call__(self):
        pass # TODO


class UpdateWidgetOfPerson(RestImplBase):
    def __init__(self, SafeSession, User, Picture, Widget, WidgetUser):
        super(UpdateWidgetOfPerson, self).__init__(SafeSession, User, Picture, Widget, WidgetUser)

    def __call__(self, username, widget, position, context):
        pass  # TODO


class NewWidget(RestImplBase):
    def __init__(self, SafeSession, User, Picture, Widget, WidgetUser):
        super(NewWidget, self).__init__(SafeSession, User, Picture, Widget, WidgetUser)

    def __call__(self, widget, base_url):
        pass  # TODO

# TODO delete widgets; reset


class Status(RestImplBase):
    def __init__(self, SafeSession, User, Picture, Widget, WidgetUser):
        super(Status, self).__init__(SafeSession, User, Picture, Widget, WidgetUser)

    def __call__(self):
        return True  # TODO (with singleton which stores state)
