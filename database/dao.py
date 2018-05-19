from database import SafeSession, User, Widget, WidgetUser, Picture
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
            user = safe_session.query(User).filter_by(username=username).first()
            safe_session.delete(user)
            safe_session.commit()

    def insert_user(self):
        pass


class PictureDao:
    def get_paths_by_username(self, username):
        path_list = []
        with SafeSession() as safe_session:
            try:
                path_list = safe_session.get_session().query(Picture).filter_by(username=username).all()
            except (SQLAlchemyError, DBAPIError) as e:
                raise DBException(str(e))
        return path_list


class WidgetDao:
    pass


class WidgetUserDao:
    pass