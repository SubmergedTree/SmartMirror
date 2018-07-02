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


@app.route("/newUser", methods=["POST"])
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
    for x in range(1, number_of + 1):
        images.append(request.files[str(x)])

    result, status = rest_impl_broker.add_picture(username, images, save_image)
    guarded_executor.unlock()
    return result, status


@app.route("/getWidgets", methods=["GET"])
def get_widgets():
    guarded_executor.lock()
    result, status = rest_impl_broker.get_widgets()
    guarded_executor.unlock()
    return jsonify(result), status


@app.route("/newWidget", methods=["POST"])
def new_widget():
    guarded_executor.lock()
    widget = request.form['widget']
    base_url = request.form['baseUrl']
    result, status = rest_impl_broker.new_widget(widget, base_url)
    guarded_executor.unlock()
    return result, status


@app.route("/deleteWidget", methods=["Delete"])
def delete_widget():
    guarded_executor.lock()
    widget = request.form['widget']
    result, status = rest_impl_broker.delete_widget(widget)
    guarded_executor.unlock()
    return result, status


@app.route("/updateWidget", methods=["POST", "DELETE"])  # TODO rename in updateWidgetMapping
def update_widget():
    result = None
    status = None
    guarded_executor.lock()
    if request.method == 'GET':
        username = request.form['username']
        widget = request.form['widget']
        position = request.form['position']
        context = request.form['context']
        result, status = rest_impl_broker.update_widget_of_user(username, widget, position, context)
    elif request.method == 'DELETE':
        username = request.form['username']
        position = request.form['position']
        result, status = rest_impl_broker.delete_widget_of_user(username, position)
    guarded_executor.unlock()
    return jsonify(result), status


@app.route("/status", methods=["GET"])
def status():
    guarded_executor.lock()
    result, status = rest_impl_broker.status()
    guarded_executor.unlock()
    return jsonify(result), status


def save_image(img, directory, name):
    path = secure_filename(name)
    path = directory + '/' + path
    img.save(path)
    return path