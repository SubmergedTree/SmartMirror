import sqlite3
from sqlite3 import Error

# TODO: Use Views
# TODO: raise custom exceptions instead of raise old
# TODO: better solution for determine if db already exists

DATABASE_PATH = "mirror_database.db"

class CreateDatabase():
    def __enter__(self):
        try:
            self.__conn = sqlite3.connect(DATABASE_PATH)
        except Error as e:
            raise
        return self
    def __exit__(self,type,value,traceback):
        self.__conn.close()    
        
    def create_database(self):
        sql_person = """CREATE TABLE IF NOT EXISTS persons(
                    username TEXT Primary KEY,
                    prename TEXT,
                    name TEXT
                    );"""

        sql_pictures_to_person = """CREATE TABLE IF NOT EXISTS pictures_to_person(
                    username TEXT,
                    image_path TEXT,
                        CONSTRAINT fk_departments FOREIGN KEY (username) REFERENCES persons(username)
                            ON DELETE CASCADE
                    );"""

        sql_widgets = """CREATE TABLE IF NOT EXISTS widgets(
                    widget TEXT PRIMARY KEY
                    );"""

        sql_widget_to_person = """CREATE TABLE IF NOT EXISTS widget_to_person(
                    username TEXT,
                    widget TEXT,
                        CONSTRAINT fk_persons FOREIGN KEY (username) REFERENCES persons(username)
                            ON DELETE CASCADE
                        CONSTRAINT fk_widgets FOREIGN KEY (widget) REFERENCES widgets(widget)
                            ON DELETE CASCADE
                    );"""
        try:
            c = self.__conn.cursor()
            c.execute(sql_person)
            c.execute(sql_pictures_to_person)
            c.execute(sql_widgets)
            c.execute(sql_widget_to_person)
            self.__conn.commit()
        except Error as e:
            self.__conn.rollback()
            #print("error on create_database")
            #raise
        
    def reset_database(self):
        pass    
    
    
class DatabaseAccess():
    def __init__(self):
        pass    