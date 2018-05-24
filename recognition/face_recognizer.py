from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot
import cv2
import os
import numpy as np
import queue

from database.dao import UserDao, DBException
from util.logger import Logger

# '/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml'


def detect_face_from_image(image, cascade_classifier_path):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cascade_classifier_path)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.2, minNeighbors=5)  # TODO remove magic numbers
    if len(faces) == 0:
        return None, None
    (x, y, w, h) = faces[0]
    return gray_image[y:y+w, x:x+h], faces[0]


class Learner(QRunnable):
    def __init__(self, learning_signals, cascade_classifier_path, user_dao, picture_dao):
        super(Learner, self).__init__()
        self.finished_learning_signal = learning_signals.finished_learning
        self.learning_error_signal = learning_signals.learning_error
        self.__cascade_classifier_path = cascade_classifier_path
        self.__user_dao = user_dao
        self.__picture_dao = picture_dao

    def run(self):
        users = self.__get_users()
        if not users:
            return
        faces, labels = self.__get_labels_faces(users)
        Logger.info("start learning")
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.train(faces, np.array(labels))
        Logger.info("finished learning")
        self.finished_learning_signal.emit(users, face_recognizer)
               
    def __get_users(self):
        users = None
        #with SafeSession() as safe_session:
        #    users = safe_session.get_session().query(User).all()
        try:
            users = self.__user_dao.get_all_user()
        except DBException as e:
            self.learning_error_signal.emit(e)
        return users
    
    def __get_picture_paths_by_username(self, username):  # TODO
        picture_paths = None
        #with SafeSession() as safe_session:
        #    assigned_user = safe_session.get_session().query(Picture).filter_by(username=username)
        try:
            picture_paths = self.__picture_dao.get_paths_by_username(username)
        except DBException as e:
            self.__learning_error_signal.emit(e)
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
                face, rect = detect_face_from_image(cv2.imread(path.image_path), self.__cascade_classifier_path)
                if face is not None:
                    labels.append(label_counter)
                    faces.append(face) 
        return faces, labels            


class Recognizer(QRunnable):
    def __init__(self, camera, users, face_recognizer, recognized_signals):
        super(Recognizer, self).__init__()
        self.__camera = camera
        self.__recognizable_users = users
        self.__face_recognizer = face_recognizer
        self.recognized_user_signal = recognized_signals.user_recognized
        self.recognizer_halt_signal = recognized_signals.recognizer_halt
        self.recognize = True

    def run(self):
        has_found = False
        while has_found is False and self.recognize is True:
            captured_image = self.__camera.capture_face()
            has_found, found_user = self.__predict(captured_image, self.__recognizable_users)          
            if has_found:
                self.recognized_user_signal.emit(found_user)

        if self.recognize is False:
            self.recognizer_halt_signal.emit()
            
    def __predict(self, captured_image, user):
        label = 0
        try:
            label, confidence = self.__face_recognizer.predict(captured_image)
        except:
            return False, ''    
        return True, user[label]


class FaceRecognizerSignals(QObject):
    user_recognized = pyqtSignal(str)
    recognizer_halt = pyqtSignal()


class FaceLearnerSignals(QObject):
    finished_learning = pyqtSignal(list, object)
    learning_error = pyqtSignal(Exception)


class FaceRecognizerScheduler(QObject):
    def __init__(self, thread_pool, camera, cascade_classifier_path,is_learning_callback, finished_learning_callback,
                 user_recognized_callback, user_dao, picture_dao):
        super(FaceRecognizerScheduler, self).__init__()
        Logger.info("faceRecognizerScheduler")
        self.__camera = camera
        self.__cascade_classifier_path = cascade_classifier_path

        self.__is_learning_callback = is_learning_callback
        self.__finished_learning_callback = finished_learning_callback
        self.__user_recognized_callback = user_recognized_callback

        self.__thread_pool = thread_pool 
        self.__learn_queue = queue.Queue() 
        self.__recognizer = None
        self.__user_list = None
        self.__face_recognizer_cv = None
        self.__is_learning = False
        self.is_showing_widgets = False

        self.__user_dao = user_dao
        self.__picture_dao = picture_dao

        self.__panic = False
        
        self.learn()
        self.schedule()

    def learn(self):
        learner = Learner(FaceLearnerSignals(), self.__cascade_classifier_path, self.__user_dao, self.__picture_dao)
        learner.finished_learning_signal.connect(self.__finished_learning)
        learner.learning_error_signal.connect(self.__error_on_learning)
        self.__learn_queue.put(learner)
        if self.__recognizer:
            self.__recognizer.recognize = False

    def schedule(self):
        if self.__is_learning or self.__panic:
            return
        elif not self.__learn_queue.empty():
            self.__recognizer = None
            self.__is_learning = True
            self.__is_learning_callback()
            self.__thread_pool.start(self.__learn_queue.get())
        else:
            self.__recognizer = Recognizer(self.__user_list, self.__face_recognizer_cv, FaceRecognizerSignals())
            self.__recognizer.recognized_user_signal.connect(self.__user_recognized)
            self.__recognizer.recognizer_halt_signal.connect(self.__recognizer_halt)
            self.__thread_pool.start(self.__recognizer)
    
    @pyqtSlot(list, object)
    def __finished_learning(self, user_list, face_recognizer):
        Logger.info("called finished_learning")
        self.__is_learning = False
        while self.is_showing_widgets:
            pass
        self.__finished_learning_callback()
        self.__user_list = user_list
        self.__face_recognizer_cv = face_recognizer
        self.schedule()                   

    @pyqtSlot(str)
    def __user_recognized(self, username):
        self.__user_recognized_callback(username)

    @pyqtSlot()
    def __error_on_learning(self, e):
        self.__panic = True
        raise e

    @pyqtSlot()
    def __recognizer_halt(self):
        self.schedule()


# Possibilities
# 1. initial learn (x)
# 2. learn triggered by API when recognizing 
# 3. learn triggered by API during show widgets (x)
# 4. triggered learning during learning (x)
# 5. recognize triggered after learning (x)
# 6. recognize triggered after show widgets (x)        