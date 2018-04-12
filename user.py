from database import DatabaseAccess
import json


class User():
    def __init__(self, name, prename, username):
        self.__name = name
        self.__prename = prename
        self.__username = username
        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        
    @property
    def prename(self):
        return self.__prename

    @prename.setter
    def prename(self, value):
        self.__prename = value
        
    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value  
        

class UserConverter():    
    def __fill_dict(self, user_list):
        new_list = []
        for user in user_list:          
            user_dict = {"username": user.username, "prename": user.prename, "name": user.name}  
            new_list.append(user_dict)
        return new_list#{"users" : new_list}new_list    
      
    def get_json(self, user_list):
        user_dict = self.__fill_dict(user_list)
        return json.dumps(user_dict)
    
    def get_user(self, json_str):
        user_dict = json.loads(json_str)
        user_res = User(user_dict["name"], user_dict["prename"], user_dict["username"])
        return user_res
    
    def get_delete_user(self, json_str):
        delete_user_dict = json.loads(json_str)
        return delete_user_dict["username"]
        
class GetWidgetsTO():
    def __init__(self):
        pass    
            

class UserDao():
    def __init__(self):
        pass
    def new_user(self, user):
        with DatabaseAccess() as da:
            return da.insert_user((user.username, user.prename, user.name))  
        return False 
    
    def get_users(self):
        user_tuple_list = []
        user_list = []
        with DatabaseAccess() as da:
            user_tuple_list = da.get_users()
        for u in user_tuple_list:
            user = User(u[2], u[1], u[0])
            user_list.append(user)
        return user_list    
    
    def delete_user(self, username):
        with DatabaseAccess() as da:
            return da.delete_user((username, ))
        return False              
