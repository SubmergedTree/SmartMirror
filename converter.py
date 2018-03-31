import json
import user

class GetUsersConverter():    
    def __fill_dict(self, user_list):
        new_list = []
        for user in user_list:          
            user_dict = {"username": user.username, "prename": user.prename, "name": user.name}  
            new_list.append(user_dict)
        return {"users" : new_list}    
      
    def get_json(self, user_list):
        user_dict = self.__fill_dict(user_list)
        return json.dumps(user_dict)
    
    def get_user(self, json):
        user_dict = json.loads(json)
        user = User(user_dict["name"], user_dict["prename"], user_dict["username"])
        return user
        
class GetWidgetsTO():
    def __init__(self):
        pass    
    