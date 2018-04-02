import json
import user

class GetUsersConverter():    
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
        user_res = user.User(user_dict["name"], user_dict["prename"], user_dict["username"])
        return user_res
        
class GetWidgetsTO():
    def __init__(self):
        pass    
    