import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from logger import Logger


Base = declarative_base()
DB_FILENAME = 'database.db'
db_engine = None
Session = None

# TODO: Remove DAO from Tablename

class UserDao(Base):
    __tablename__ = 'UserDao'
    username = Column(String(250), primary_key=True)
    prename = Column(String(250))
    name = Column(String(250))
    pictures = relationship('PictureDao', cascade='all,delete', backref='UserDao')
    widget_person = relationship('WidgetUserDao', cascade='all,delete', backref='UserDao')


class PictureDao(Base):
    __tablename__ = 'PictureDao'
    username = Column(String(250), ForeignKey('UserDao.username'))
    image_path = Column(String(250), primary_key=True)


class WidgetDao(Base):
    __tablename__ = 'WidgetDao'
    widget = Column(String(250), primary_key=True)
    widget_person = relationship('WidgetUserDao', cascade='all,delete', backref='WidgetDao')


class WidgetUserDao(Base):
    __tablename__ = 'WidgetUserDao'
    mapping_id = Column(Integer, primary_key=True)
    username = Column(String(250), ForeignKey('UserDao.username'))
    widget = Column(String(250), ForeignKey('WidgetDao.widget'))
    position = Column(Integer)
    context = Column(String(250))
    
    
def setup_database():
    global Session, db_engine
    
    def is_db_already_created():
        to_test = Path(DB_FILENAME)
        return to_test.is_file()
    
    def fill_widgets():
        joke = WidgetDao(widget='Joke')
        wheater_today = WidgetDao(widget='WheaterToday')
        with SafeSession as session:
            session.add(joke)
            session.flush()
            session.add(wheater_today)
            session.commit()

    db_engine = create_engine('sqlite:///' + DB_FILENAME) 
    Base.metadata.create_all(db_engine)
    Session = sessionmaker(bind=db_engine) 
    if not is_db_already_created():
        Logger.info('New database created.')
        fill_widgets()   
    Logger.info('Database is ready.')


class SafeSession():
    def __enter__(self):
        self.__session = Session()
        return self
    
    def __exit__(self, type, value, traceback):
        self.__session.close()
    
    def add(self, to_add):
        self.__session.add(to_add)
    
    def flush(self):
        self.__session.flush()
        
    def commit(self):
        self.__session.commit()
    
    def delete(self, to_delete):
        self.__session.delete(to_delete)
        
    def get_session(self):
        return self.__session

   
setup_database()  


