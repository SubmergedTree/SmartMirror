from flask import Flask, jsonify, request
from werkzeug import secure_filename
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, QThread
from database.database import User, SafeSession, Picture, WidgetUser, Widget
from util.logger import Logger
from datetime import datetime
from util.guarded_executor import GuardedExecutor
from api.rest_impl import RestBroker
# TODO: need to catch exception and return suitable status when errors occur.
# e.g. server is knocked out by creating duplicated user (it restarts itself but client receives a 500)

app = Flask(__name__)
PORT = 5000


class HttpStatus:
    SUCCESS = 200
    CREATED = 201
    BADREQUEST = 400
    FORBIDDEN = 403
    NOTFOUND = 404
    CONFLICT = 409
    INTERNALSERVERERROR = 500


guarded_executor = None


class RestApiSignal(QObject):
    new_pictures = pyqtSignal()


new_picture_signal = None

rest_broker = RestBroker(SafeSession=SafeSession,
                         User=User,
                         Picture=Picture,
                         Widget=Widget,
                         WidgetUser=WidgetUser)


class RestApiExp(QThread):
    def __init__(self, signal):
        super(RestApiExp, self).__init__()
        global new_picture_signal, guarded_executor
        new_picture_signal = signal
        guarded_executor = GuardedExecutor(lambda: super(RestApiExp, self).terminate())

    def run(self):
        app.run(host='0.0.0.0', port=PORT, debug=False)

    def shut_down(self):
        guarded_executor.try_to_exec()


class RestApi(QRunnable): 
    def __init__(self, signal):
        super(RestApi, self).__init__()
        global new_picture_signal
        new_picture_signal = signal

    def run(self):
        app.run(host='0.0.0.0', port=PORT, debug=False)

    def shut_down(self):
        func_s_d = request.environ.get('werkzeug.server.shutdown')
        if func_s_d is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func_s_d()


@app.route("/getUsers", methods=["GET"])
def get_users():
    guarded_executor.lock()
    Logger.info('request: getUsers.')
    user_list = rest_broker.get_users()
    guarded_executor.unlock()
    return jsonify(user_list), HttpStatus.SUCCESS


@app.route("/newUser", methods=["POST"])  # TODO 1 picture needed
def new_user():
    guarded_executor.lock()
    Logger.info('request: newUser.')
    username = request.form['username']
    prename = request.form['prename']
    name = request.form['name']
    success = rest_broker.new_user(username, prename, name)
    return (jsonify('User successfully created'), HttpStatus.CREATED) if success \
        else (jsonify('Duplicated User'), HttpStatus.CONFLICT)


@app.route("/deleteUser", methods=["DELETE"])
def delete_user():
    guarded_executor.lock()
    Logger.info('request: deleteUser.')
    username = request.form['username']
    success = rest_broker.delete_user(username)
    guarded_executor.unlock()
    return (jsonify('User successfully deleted'), HttpStatus.CREATED) if success \
        else (jsonify('User does not exist'), HttpStatus.CONFLICT)


@app.route("/addPicture", methods=["POST"])
def add_picture():
    guarded_executor.lock()
    Logger.info('request: addPictures.')
    username = request.form['username']
    Logger.info(username)
    image = request.files['image']
    Logger.info(image.filename)
    image_name = username + str(datetime.now())
    image = request.files['image']
    image.save(secure_filename(image_name))
    with SafeSession() as safe_session:
        assigned_user = safe_session.get_session().query(User).filter_by(username=username).first() 
        if assigned_user == None:
            return jsonify('User: ' + username + ' does not exist'), HttpStatus.NOTFOUND
        picture_to_store = Picture(username=assigned_user.username, image_path=image_name) 
        safe_session.add(picture_to_store)
        safe_session.commit()
        new_picture_signal.emit()
    guarded_executor.unlock()
    return jsonify('Picture successfully added'), HttpStatus.CREATED 
   

@app.route("/getWidgets", methods=["GET"])
def get_widgets():
    guarded_executor.lock()
    Logger.info('request: getWidgets.')
    guarded_executor.unlock()
    return jsonify(("username", "email"))


@app.route("/updateWidgets", methods=["POST"])
def update_widgets():
    guarded_executor.lock()
    Logger.info('request: updateWidgets.')
    guarded_executor.unlock()
    return jsonify(("username", "email"))


@app.route("/health", methods=["GET"])
def health():
    guarded_executor.lock()
    guarded_executor.unlock()
    return jsonify({"health": "healthy"})