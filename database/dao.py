from database.database import SafeSession, User, Widget, WidgetUser, Picture
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError
from sqlalchemy import func


class DBException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserDao:

    def get_user_by_username(self, username):
        assigned_user = None
        with SafeSession() as safe_session:
                try:
                    assigned_user = safe_session.get_session().query(User).filter_by(username=username).first()
                except (SQLAlchemyError, DBAPIError) as e:
                    raise DBException(str(e))
        return assigned_user

    def get_all_user(self):
        users = []
        with SafeSession() as safe_session:
            try:
                users = safe_session.get_session().query(User).all()
            except (SQLAlchemyError, DBAPIError) as e:
                raise DBException(str(e))
        return users

    def delete_user_by_username(self, username):
        with SafeSession() as safe_session:
            try:
                user_to_delete = safe_session.get_session().query(User).filter_by(username=username).first()
                if user_to_delete:
                    safe_session.delete(user_to_delete)
                    safe_session.commit()
                    return True
                else:
                    return False
            except (SQLAlchemyError, DBAPIError) as e:
                safe_session.rollback()
                raise DBException(str)

    def insert_user(self, username, prename, name):
        with SafeSession() as safe_session:
            try:
                if safe_session.get_session().query(User).filter_by(username=username).first() is None:
                    user = User(username=username, prename=prename, name=name)
                    safe_session.add(user)
                    safe_session.commit()
                    return True
                else:
                    return False
            except (SQLAlchemyError, DBAPIError) as e:
                safe_session.rollback()
                raise DBException(str)


class PictureDao:

    def get_number_of_pictures_per_username(self, username):
        number_of = []
        with SafeSession() as safe_session:
            try:
                number_of = safe_session.get_session().query(Picture).filter_by(username=username).count()
            except (SQLAlchemyError, DBAPIError) as e:
                raise DBException(str(e))
        return number_of

    def get_paths_by_username(self, username):
        path_list = []
        with SafeSession() as safe_session:
            try:
                path_list = safe_session.get_session().query(Picture).filter_by(username=username).all()
            except (SQLAlchemyError, DBAPIError) as e:
                raise DBException(str(e))
        return path_list

    def add_picture(self, username, image_path):
        with SafeSession() as safe_session:
            try:
                user = safe_session.get_session().query(User).filter_by(username=username).first()
                if user:
                    picture = Picture(username=user.username, image_path=image_path)
                    safe_session.add(picture)
                    safe_session.commit()
                    return True
                else:
                    return False
            except (SQLAlchemyError, DBAPIError) as e:
                safe_session.rollback()
                raise DBException(str)


class WidgetDao:

    def get_base_url(self, widget):
        url = None
        with SafeSession() as safe_session:
                try:
                    widget = safe_session.get_session().query(Widget).filter_by(widget=widget).first()
                    if widget:
                        url = widget.base_url
                except (SQLAlchemyError, DBAPIError) as e:
                    raise DBException(str(e))
        return url

    def get_widgets(self):
        widgets = []
        with SafeSession() as safe_session:
            try:
                tuple_widgets = safe_session.get_session().query(Widget.widget).all()
                for item in tuple_widgets:
                    widgets.append(item[0])
            except (SQLAlchemyError, DBAPIError) as e:
                raise DBException(str(e))
        return widgets

    def add_widget(self, widget, base_url):
        ret = None
        with SafeSession() as safe_session:
            try:
                if safe_session.get_session().query(Widget).filter_by(widget=widget).first() is None:
                    widget = Widget(widget=widget, base_url=base_url)
                    safe_session.add(widget)
                    safe_session.commit()
                    ret = True
                else:
                    ret = False
            except (SQLAlchemyError, DBAPIError) as e:
                safe_session.rollback()
                raise DBException(str)
        return ret

    def delete_widget(self, widget):
        with SafeSession() as safe_session:
            try:
                widget_to_delete = safe_session.get_session().query(Widget).filter_by(widget=widget).first()
                if widget_to_delete:
                    safe_session.delete(widget_to_delete)
                    safe_session.commit()
                    return True
                else:
                    return False
            except (SQLAlchemyError, DBAPIError) as e:
                safe_session.rollback()
                raise DBException(str)

    def does_widget_exists(self, widget_name):
        result = False
        with SafeSession() as safe_session:
                try:
                    widget = safe_session.get_session().query(Widget).filter_by(widget=widget_name).first()
                    if widget:
                        result = True
                except (SQLAlchemyError, DBAPIError) as e:
                    raise DBException(str(e))
        return result


class WidgetUserDao:

    def get_mapping(self, username):
        mapping_list = []
        with SafeSession() as safe_session:
            try:
                mapping_list = safe_session.get_session().query(WidgetUser).filter_by(username=username).all()
            except (SQLAlchemyError, DBAPIError) as e:
                raise DBException(str(e))
        return mapping_list

    def update(self, widget, username, position, context):  # TODO refactor lazy implementation
        identifier = username + str(position)
        self.delete(identifier)
        success = False
        with SafeSession() as safe_session:
            try:
                if WidgetDao().does_widget_exists(widget):
                    widget_user = WidgetUser(identifier=identifier,widget=widget,
                                             username=username, position=position, context=context)
                    safe_session.add(widget_user)
                    safe_session.commit()
                    success = False
            except (SQLAlchemyError, DBAPIError, DBException) as e:
                safe_session.rollback()
                raise DBException(str)
        return success

    def delete(self, identifier):
        success = False
        with SafeSession() as safe_session:
            try:
                mapping_to_delete = safe_session.get_session().query(WidgetUser).filter_by(identifier=identifier).first()
                if mapping_to_delete:
                    safe_session.delete(mapping_to_delete)
                    safe_session.commit()
                    success =  True
            except (SQLAlchemyError, DBAPIError) as e:
                safe_session.rollback()
                raise DBException(str)
        return success

