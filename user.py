from database import DatabaseAccess

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
            user = User(u[0], u[1], u[2])
            user_list.append(user)
        return user_list    
    
    def delete_user(self, user):
        with DatabaseAccess() as da:
            return da.delete_user((user.username, ))
                      
