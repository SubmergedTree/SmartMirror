import sqlite3
from sqlite3 import Error

import os

# TODO: Use Views
# TODO: better solution to determine if db already exists

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
        sql_person = """
                    CREATE TABLE IF NOT EXISTS persons(
                    username TEXT Primary KEY,
                    prename TEXT,
                    name TEXT
                    );"""

        sql_pictures_to_person = """
                    CREATE TABLE IF NOT EXISTS pictures_to_person(
                    username TEXT,
                    image_path TEXT,
                        CONSTRAINT fk_persons FOREIGN KEY (username) REFERENCES persons(username)
                            ON DELETE CASCADE
                    );"""

        sql_widgets = """                 
                    CREATE TABLE IF NOT EXISTS widgets(
                    widget TEXT PRIMARY KEY
                    );"""

        sql_widget_to_person = """
                    CREATE TABLE IF NOT EXISTS widget_to_person(
                    username TEXT,
                    widget TEXT,
                    position INTEGER,
                        CONSTRAINT fk_persons FOREIGN KEY (username) REFERENCES persons(username)
                            ON DELETE CASCADE,
                        CONSTRAINT fk_widgets FOREIGN KEY (widget) REFERENCES widgets(widget)
                            ON DELETE CASCADE
                    );"""
        try:
            c = self.__conn.cursor()
            c.execute("PRAGMA foreign_keys = 1")
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
        os.remove(DATABASE_PATH)
        try:
            self.__conn = sqlite3.connect(DATABASE_PATH)
        except Error as e:
            raise
        self.create_database()    
        print("db resetted")
    
    
class DatabaseAccess():
    def __enter__(self):
        try:
            self.__conn = sqlite3.connect(DATABASE_PATH)
            c = self.__conn.cursor()
            c.execute("PRAGMA foreign_keys = 1") 
        except Error as e:
            raise
        return self
    
    def __exit__(self,type,value,traceback):
        self.__conn.close()
        
    def insert_picture(self, data):
        sql = '''INSERT INTO pictures_to_person(username, image_path)
                 VALUES(?, ?)'''
        self.__transact(sql, data, "insert_picture")

            
    def get_pictures_path(self, data):
        sql = '''SELECT image_path FROM pictures_to_person 
                 WHERE username = ?'''     
        return self.__select_execute(sql, data, "get_pictures_path")

            
    def insert_user(self, data):
        sql = '''INSERT INTO persons(username, prename, name)
                 VALUES(?, ?, ?)'''
        return self.__transact(sql, data, "insert_user")
              
     
    def get_users(self):
        sql = '''SELECT * FROM persons'''   
        return self.__select_execute_without_params(sql, "get_users")
            
    def delete_user(self, data):
        sql = '''DELETE FROM persons WHERE username = ?'''
        self.__transact(sql, data, "delete_user")

            
    def add_widget(self, data):
        sql = '''INSERT INTO widgets(widget)
                 VALUE(?)'''
        self.__transact(sql, data, "add_widget")

              
    def remove_widget(self, data):
        sql = '''DELETE FROM widgets WHERE widget = ?'''
        self.__transact(sql, data, "remove_widget")
 
            
    def get_widgets(self):
        sql = '''SELECT * FROM widgets'''   
        return self.__select_execute_without_params(sql, "get_widgets")
            
    
    def add_widget_to_user(self, data):
        sql = '''INSERT INTO widget_to_person(username, widget, position)'''
        self.__transact(sql, data, "add_widget_to_user")
        
    
    def remove_all_widgets_from_user(self, data):
        sql = '''DELETE FROM widget_to_person WHERE username = ?'''
        self.__transact(sql, data, "remove_all_widgets_from_user")
                
    def update_widget_from_user(self, data):
        pass  
    
    def get_widgets_from_user(self, data):
        sql = '''SELECT * FROM widget_to_person WHERE username = ?'''   
        return self.__select_execute(sql, data, "get_widgets_from_user")
            
    def __select_execute_without_params(self, sql, fname):
        try:
            c = self.__conn.cursor()  
            c.execute(sql)
            return c.fetchall()
        except Error as e:
            print("error on " + fname)
            print(e) 
    
    def __select_execute(self, sql, data, fname):
        try:
            c = self.__conn.cursor()  
            c.execute(sql, data)
            return c.fetchall()
        except Error as e:
            print("error on " + fname)
            print(e) 
    
    def __transact(self, sql, data, fname):
        try:
            c = self.__conn.cursor() 
            c.execute(sql, data)
            self.__conn.commit()
            return True    
        except Error as e:
            self.__conn.rollback()
            print("error on " + fname)
            print(e)
            return False
                                             
               
#######################################
###              Tests              ###
####################################### 

#with CreateDatabase() as cd:
#    cd.reset_database()
#     
# def test_insert_get_picture():
#     with DatabaseAccess() as da:
#         da.insert_picture(("username", "path_to_picture"))
#     with DatabaseAccess() as da:
#         da.insert_picture(("username", "path_to_picture2"))
#     with DatabaseAccess() as da:
#         da.insert_picture(("blub", "path_to_picture2_blub"))
#     with DatabaseAccess() as da:
#         print(da.get_pictures_path(("username",)))
# 
# def test_add_get_user():
#     with DatabaseAccess() as da:
#         da.insert_user(("username", "prename", "name"))
#         da.insert_user(("username1", "prename1", "name1s"))
#         da.insert_user(("blub", "prename1", "name1s"))
#     with DatabaseAccess() as da:
#         print(da.get_users())
# 
# 
# def test_add_similar_but_different_username_user():
#     with DatabaseAccess() as da:
#         da.insert_user(("username2", "prename", "name"))
#         da.insert_user(("username3", "prename", "name"))
#         print(da.get_users())
# 
# def test_insert_equal_user():
#     with DatabaseAccess() as da:
#         da.insert_user(("username4", "prename", "name"))
#         da.insert_user(("username4", "prename", "name"))        
# 
# def test_delete_user():
#     with DatabaseAccess() as da:
#         da.delete_user(("username", ))
#         print(da.get_users())
#         print(da.get_pictures_path(("username",)))
#         
# #def test_        
# 
# 
# print(sqlite3.sqlite_version)
# 
# print("   test1     ")
# test_add_get_user()
# print("    test2    ")
# test_insert_get_picture()
# print("   test3     ")
# test_add_similar_but_different_username_user() 
# print("    test4    ")
# test_insert_equal_user()
# print("    test5    ")
# test_delete_user()  
#            