from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import queue

import cv2
from database.database import *
from database.dao import DBException
import numpy as np
from util.path import path_points_to_file

CASCADE_SCALE_FACTOR = 1.2
CASCADE_MIN_NEIGHBORS = 5

def detect_face_from_image(image, cascade_classifier_path):
    #if not image:
    #    return None, None
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cascade_classifier_path)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=CASCADE_SCALE_FACTOR, minNeighbors=CASCADE_MIN_NEIGHBORS)
    if len(faces) == 0:
        return None, None
    (x, y, w, h) = faces[0]
    return gray_image[y:y+w, x:x+h], faces[0]


class LearnerSignals(QObject):
    finished_learning = pyqtSignal(list, object)
    learning_error = pyqtSignal(Exception)
    no_training_data = pyqtSignal()


class RecognizerSignals(QObject):
    user_recognized = pyqtSignal(str)
    recognizer_halt = pyqtSignal()


class Learner(QRunnable):
    def __init__(self, cascade, signals, user_dao, picture_dao):
        super(Learner, self).__init__()
        self.signals = signals
        self.user_dao = user_dao
        self.picture_dao = picture_dao
        self.__cascade_classifier_path = cascade

    def run(self):
        try:
            users = self.user_dao.get_all_user()
            users[:] = [user for user in users if
                        self.picture_dao.get_number_of_pictures_per_username(user.username) > 0]
            if len(users) == 0:
                self.signals.no_training_data.emit()
                return
        except DBException as e:
            self.signals.learning_error.emit(e)
            return
        faces, labels = self.__get_labels_faces(users)
        if len(faces) == 0 or len(labels) == 0:
            self.signals.no_training_data.emit()
            return
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.train(faces, np.array(labels))

        self.signals.finished_learning.emit(users, face_recognizer)  # Return the result of the processing

    def __get_picture_paths_by_username(self, username):
        picture_paths = None
        try:
            picture_paths = self.picture_dao.get_paths_by_username(username)
        except DBException as e:
            self.signals.learning_error.emit(e)
        return picture_paths

    def __get_labels_faces(self, users):
        labels = []
        faces = []
        label_counter = 0
        for user in users:
            path_list = self.__get_picture_paths_by_username(user.username)
            if not path_list:
                return
            label_counter += 1
            for path in path_list:
                if path_points_to_file(path.image_path):
                    face, rect = detect_face_from_image(cv2.imread(path.image_path), self.__cascade_classifier_path)
                    if face is not None:
                        labels.append(label_counter)
                        faces.append(face)
        return faces, labels


class Recognizer(QRunnable):
    def __init__(self, signals, face_recognizer, users, camera):
        super(Recognizer, self).__init__()
        self.signals = signals
        self.camera = camera
        self.users = users
        self.camera = camera
        self.face_recognizer = face_recognizer
        self.recognize = True

    def __predict(self, captured_image, user):
        try:
            label, confidence = self.face_recognizer.predict(captured_image)
        except:
            return False, ''
        return (True, user[label]) if confidence <= 50 else (False, '')

    def run(self):
        has_found = False
        while has_found is False and self.recognize is True:
            captured_image = self.camera.capture_face()
            has_found, found_user = self.__predict(captured_image, self.users)
            if has_found:
                self.camera.stop()
                self.signals.user_recognized.emit(found_user.username)
        if self.recognize is False:
            self.camera.stop()
            self.signals.recognizer_halt.emit()

    def stop_recognizer(self):
        self.camera.stop()
        self.recognize = False


class Scheduler(QObject):
    def __init__(self, user_dao, picture_dao, camera, cascade,
                 is_learning_callback, finished_learning_callback,
                 no_training_data_cb, user_recognized_callback,
                 learning_error_cb):
        super(Scheduler, self).__init__()
        self.user_dao = user_dao
        self.picture_dao = picture_dao

        self.threadpool = QThreadPool()
        #print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.queue = queue.Queue()

        self.queue.put(Learner(cascade, LearnerSignals(), user_dao, picture_dao))
        self.recognizer = None
        self.panic = False
        self.is_learning = False
        self.is_recognizing = False
        self.face_recognizer = False
        self.is_shut_down = False
        self.users = None
        self.camera = camera
        self.cascade = cascade

        self.is_learning_callback = is_learning_callback
        self.finished_learning_callback = finished_learning_callback
        self.user_recognized_callback = user_recognized_callback
        self.no_training_data_callback = no_training_data_cb
        self.learning_error_callback = learning_error_cb

        self.schedule()


    @pyqtSlot(list, object)
    def finished_learning(self, user, f_r):
        Logger.info('Finished learning')
        self.is_learning = False
        self.finished_learning_callback()
        self.face_recognizer = f_r
        user.insert(0, "")
        self.users = user
        self.schedule()

    @pyqtSlot()
    def learning_error(self, e):
        Logger.warn('Learning error')
        self.is_learning = False
        self.panic = True
        self.learning_error_callback()

    @pyqtSlot(str)
    def recognized_user(self, username):
        Logger.info("user: {} recognized".format(username))
        self.is_recognizing = False
        self.user_recognized_callback(username)

    @pyqtSlot()
    def recognizer_halt(self):
        Logger.info("recognizer halt")
        self.is_recognizing = False
        if not self.is_shut_down:
            self.schedule()

    @pyqtSlot()
    def no_training_data(self):
        Logger.warn('No training data')
        self.is_learning = False
        self.no_training_data_callback()

    def learn(self):
        Logger.info('Learn request')
        self.queue.put(Learner(self.cascade, LearnerSignals(), self.user_dao, self.picture_dao))
        if self.recognizer:
            self.recognizer.stop_recognizer()
        self.schedule()

    def schedule(self):
        if self.panic is True or self.is_learning or self.is_recognizing:
            return
        if not self.queue.empty():
            Logger.info('Is learning')
            self.is_learning = True
            self.is_learning_callback()
            current_learner = self.queue.get()
            current_learner.signals.finished_learning.connect(self.finished_learning)
            current_learner.signals.learning_error.connect(self.learning_error)
            current_learner.signals.no_training_data.connect(self.no_training_data)
            self.threadpool.start(current_learner)
        else:
            Logger.info('Is recognizing')
            self.is_recognizing = True
            self.recognizer = Recognizer(RecognizerSignals(), self.face_recognizer, self.users, self.camera)
            self.recognizer.signals.user_recognized.connect(self.recognized_user)
            self.recognizer.signals.recognizer_halt.connect(self.recognizer_halt)
            self.threadpool.start(self.recognizer)

    def shut_down(self):
        Logger.info('Shut down face recognition')
        self.is_shut_down = True
        if self.recognizer:
            self.recognizer.stop_recognizer()
        self.threadpool.waitForDone()
