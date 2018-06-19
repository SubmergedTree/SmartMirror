from database.database import SafeSession, User, Widget, WidgetUser, Picture
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError


class DBException(Exception):
    pass


class UserDao:

    def get_user_by_username(self, username):
        assigned_user = None
        with SafeSession() as safe_session:
                try:
                    assigned_user = safe_session.get_session().query(Picture).filter_by(username=username)
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
                if safe_session.get_session().query(Picture).filter_by(username=username).first() is None:
                    picture = Picture(username=username, image_path=image_path)
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
                    widget = safe_session.get_session().query(Picture).filter_by(widget=widget)
                    url = widget.base_url
                except (SQLAlchemyError, DBAPIError) as e:
                    raise DBException(str(e))
        return url

    def get_widgets(self):
        widgets = []
        with SafeSession() as safe_session:
            try:
                widgets = safe_session.get_session().query(Widget).all()
            except (SQLAlchemyError, DBAPIError) as e:
                raise DBException(str(e))
        return widgets

    def add_widget(self, widget, base_url):
        with SafeSession() as safe_session:
            try:
                if safe_session.get_session().query(Widget).filter_by(widget=widget).first() is None:
                    widget = Widget(widget=widget, base_url=base_url)
                    safe_session.add(widget)
                    safe_session.commit()
                    return True
                else:
                    return False
            except (SQLAlchemyError, DBAPIError) as e:
                safe_session.rollback()
                raise DBException(str)

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


class WidgetUserDao:

    def get_mapping(self, username):
        mapping_list = []
        with SafeSession() as safe_session:
            try:
                mapping = safe_session.get_session().query(WidgetUser).filter_by(username=username).all()
                mapping_list.append(mapping)
            except (SQLAlchemyError, DBAPIError) as e:
                raise DBException(str(e))
        return mapping_list

    def update(self, widget, username, position, context):  # TODO refactor lazy implementation
        self.delete(username, position)
        with SafeSession() as safe_session:
            try:
                widget_user = WidgetUser(widget=widget, username=username, position=position, context=context)
                safe_session.add(widget_user)
                safe_session.commit()
            except (SQLAlchemyError, DBAPIError) as e:
                safe_session.rollback()
                raise DBException(str)

    def delete(self, username, position):
        with SafeSession() as safe_session:
            try:
                mapping_to_delete = safe_session.get_session().query(WidgetUser)\
                    .filter(WidgetUser.username == username and WidgetUser.position == position)\
                    .first()
                if mapping_to_delete:
                    safe_session.delete(mapping_to_delete)
                    safe_session.commit()
                    return True
                else:
                    return False
            except (SQLAlchemyError, DBAPIError) as e:
                safe_session.rollback()
                raise DBException(str)
