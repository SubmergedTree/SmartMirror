from flask import Flask, jsonify, request
from PyQt5.QtCore import QThread, QObject
from database import UserDao, WidgetDao, PictureDao, WidgetUserDao, SafeSession

from logger import Logger

# TODO: need to catch exception and return suitable status when errors occur.

app = Flask(__name__)
PORT = 5000


class HttpStatus():
    SUCCESS = 200
    CREATED = 201
    BADREQUEST = 400
    FORBIDDEN = 403
    NOTFOUND = 404
    CONFLICT = 409
    INTERNALSERVERERROR = 500
    
signal_util = None    

class RestApiThread(QThread):
    def __init__(self): 
        QThread.__init__(self)
        signal_util = self
        Logger.info('Rest API is ready.')
        
    def __del__(self):
        self.wait()    
    
    def run(self):
        app.run(host='0.0.0.0', port=PORT, debug=False)    
    

@app.route("/getUsers", methods=["GET"])
def get_users():
    Logger.info('request: getUsers.')
    user_list = []
    with SafeSession() as safe_session:  
        for user in safe_session.get_session().query(UserDao):
            user_dict = {}
            user_dict['username'] = user.username
            user_dict['prename'] = user.prename
            user_dict['name'] = user.name
            user_list.append(user_dict)
        safe_session.commit()
    return jsonify(user_list), HttpStatus.SUCCESS


@app.route("/newUser", methods=["POST"])
def new_user():
    Logger.info('request: newUser.')
    username = request.form['username']
    prename = request.form['prename']
    name = request.form['name']
    user = UserDao(username=username, prename=prename, name=name)
    with SafeSession() as safe_session:
        safe_session.add(user)   
        safe_session.commit()  
    return jsonify('User successfully created'), HttpStatus.CREATED 


@app.route("/deleteUser", methods=["DELETE"])
def delete_user():
    Logger.info('request: deleteUser.')
    username = request.form['username']
    with SafeSession() as safe_session:
        user_to_delete = safe_session.get_session().query(UserDao).filter_by(username=username).first() 
        safe_session.delete(user_to_delete)
        safe_session.commit()
    return jsonify((username, email)), HttpStatus.SUCCESS


@app.route("/addPictures", methods=["POST"])
def add_picture():
    Logger.info('request: addPictures.')
    print(request.form['username'])
    return jsonify(request.form)
    

@app.route("/getWidgets", methods=["GET"])
def get_widgets():
    Logger.info('request: getWidgets.')
    return jsonify((username, email))


@app.route("/updateWidgets", methods=["POST"])
def update_widgets():
    Logger.info('request: updateWidgets.')
    return jsonify((username, email))



    