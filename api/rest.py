from flask import Flask, jsonify, request
from werkzeug import secure_filename
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, QThread
from datetime import datetime
from util.guarded_executor import GuardedExecutor
from api.rest_impl import RestBroker

app = Flask(__name__)
PORT_DEFAULT = 5000

BADREQUEST = 400

guarded_executor = None


rest_impl_broker = None


port = PORT_DEFAULT


class RestApi(QThread):
    def __init__(self, rest_broker, server_port):
        super(RestApi, self).__init__()
        global guarded_executor, rest_impl_broker, port
        guarded_executor = GuardedExecutor(lambda: super(RestApi, self).terminate())
        rest_impl_broker = rest_broker
        port = server_port

    def run(self):
        app.run(host='0.0.0.0', port=port, debug=False)

    def shut_down(self):
        guarded_executor.try_to_exec()


@app.route("/getUsers", methods=["GET"])
def get_users():
    guarded_executor.lock()
    result, status = rest_impl_broker.get_users()
    guarded_executor.unlock()
    return jsonify(result), status


@app.route("/newUser", methods=["POST"])  # TODO 1 picture needed
def new_user():
    guarded_executor.lock()
    username = request.form['username']
    prename = request.form['prename']
    name = request.form['name']
    image = request.files['image']
    result, status = rest_impl_broker.new_user(username, prename,
                                               name, image,
                                               save_image)
    guarded_executor.unlock()
    return jsonify(result), status


@app.route("/deleteUser", methods=["DELETE"])
def delete_user():
    guarded_executor.lock()
    username = request.form['username']
    result, status = rest_impl_broker.delete_user(username)
    guarded_executor.unlock()
    return jsonify(result), status


@app.route("/addPictures", methods=["POST"])
def add_pictures():
    guarded_executor.lock()
    username = request.form['username']
    try:
        number_of = int(request.form['numberOf'])
    except ValueError:
        return jsonify('Wrong arguments'), BADREQUEST
    images = []
    for x in range(0, number_of):
        images.append(request.files['images{}'.format(x)])

    #result, status = rest_impl_broker.add_picture(username, images, save_image)
    guarded_executor.unlock()
    return "foo", 200

    # image = request.files['image']
    # image_name = username + str(datetime.now())
    # image = request.files['image']
    # image.save(secure_filename(image_name))
    # with SafeSession() as safe_session:
    #     assigned_user = safe_session.get_session().query(User).filter_by(username=username).first()
    #     if assigned_user == None:
    #         return jsonify('User: ' + username + ' does not exist'), HttpStatus.NOTFOUND
    #     picture_to_store = Picture(username=assigned_user.username, image_path=image_name)
    #     safe_session.add(picture_to_store)
    #     safe_session.commit()
    #     new_picture_signal.emit()
    # guarded_executor.unlock()
    # return jsonify(result), status
   

@app.route("/getWidgets", methods=["GET"])
def get_widgets():
    guarded_executor.lock()
    result, status = rest_impl_broker.get_widgets()
    guarded_executor.unlock()
    return jsonify(result), status


@app.route("/updateWidget", methods=["POST"])
def update_widget():
    guarded_executor.lock()
    username = request.form['username']
    widget = request.form['widget']
    position = request.form['position']
    context = request.form['context']
    result, status = rest_impl_broker.update_widget_of_person(username, widget, position, context)
    guarded_executor.unlock()
    return jsonify(result), status


@app.route("/status", methods=["GET"])
def status():
    guarded_executor.lock()
    result, status = rest_impl_broker.status()
    guarded_executor.unlock()
    return jsonify(result), status


def save_image(img, name):
    path = secure_filename(name)
    img.save(path)
    return path