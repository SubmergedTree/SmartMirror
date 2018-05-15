from PyQt5.QtCore import QRunnable, pyqtSignal, pyqtSlot
import cv2
import os
import numpy as np
import queue

from camera import Camera
from database import User, Picture


def detect_face_from_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.2, minNeighbors=5)  # TODO remove magic numbers
    if len(faces) == 0:
        return None,None
    (x, y, w, h) = faces[0]
    return gray_image[y:y+w, x:x+h], faces[0]


class Learner(QRunnable):
    def __init__(self, finished_learning_signal):
        self.__finished_learning_signal = finished_learning_signal
    
    def run(self):
        users = self.__get_users()
        faces, labels = self.__get_labels_faces(users)
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.train(faces, np.array(labels))
        self.__finished_learning_signal.emit(users, face_recognizer)
               
    def __get_users(self):
        users = []
        with SafeSession() as safe_session:
            users = safe_session.get_session().query(User)
        return users
    
    def __get_picture_paths_by_username(self, username):
        picture_paths = []
        with SafeSession() as safe_session:
                assigned_user = safe_session.get_session().query(Picture).filter_by(username=username)
        return picture_paths
    
    def __get_labels_faces(self, users):
        labels = []
        faces = []
        label_counter = 0
        for user in users:
            path_list = self.__get_picture_paths_by_username(user.username)
            label_counter += 1
            for path in path_list:
                face, rect = detect_face_from_image(cv2.imread(path))
                if face is not None:
                    labels.append(label_counter)
                    faces.append(face) 
        return faces, labels            


class Recognizer(QRunnable):
    def __init__(self, users, face_recognizer, recognized_user_signal):
        self.__recognizable_users = users
        self.__face_recognizer = face_recognizer
        self.__recognized_user_signal = recognized_user_signal
        self.recognize = True

    def run(self):
        camera = Camera()
        has_found = False
        while has_found is False and self.__recognize is True:
            captured_image = camera.capture_face()   
            has_found, found_user = self.__predict(captured_image, self.__recognizable_users)          
            if has_found:
               self.__recognized_user_signal(found_user)            
            
    def __predict(self, img, user):
        label = 0
        try:
            label, confidence = self.__face_recognizer.predict(captured_image)
        except:
            return False, ''    
        return True, user[label]   


class FaceRecognizerScheduler: # TODO: keep signals internal in this module
    def __init__(self, thread_pool, is_learning_callback , finished_learning_signal, recognized_user_signal):
        self.__finished_learning_signal = finished_learning_signal
        self.__finished_learning_signal.connect(self.finished_learning)
        self.__recognized_user_signal = recognized_user_signal
        
        self.__is_learning_callback = is_learning_callback
        
        self.__thread_pool = thread_pool 
        self.__learn_queue = queue.Queue() 
        self.__recognizer = None
        
        self.__user_list = None
        self.__face_recognizer_cv = None

        self.__is_learning = True

        self.is_showing_widgets = False
        
        self.learn()
        self.schedule()
        
    def learn(self):  # We need a signal/slot to inform when recognizer is shut down -> in this slot set recognizer to None
        self.__learn_queue.put(Learner(self.__finished_learning_signal))
        if self.__recognizer:
            self.__recognizer.recognize = False
        self.schedule()
     
    def schedule(self):
        if self.__is_learning:
            return
        elif not self.__learn_queue.empty():  # TODO: wait until recognizer finished -> active waiting should do the job
            self.__recognizer = None
            self.__is_learning = True
            self.__is_learning_callback()
            self.__thread_pool.start(self.__learn_queue.get())
        else:
            self.__recognizer = Recognizer(self.__user_list, self.__face_recognizer_cv, self.__recognized_user_signal)
            self.__thread_pool.start(self.__recognizer)
    
    @pyqtSlot() 
    def finished_learning(self, user_list, face_recognizer):
        self.__is_learning = False
        while self.is_showing_widgets:
            pass
        self.__user_list = user_list
        self.__face_recognizer_cv = face_recognizer
        self.schedule()                   



# Possibilities
# 1. initial learn (x)
# 2. learn triggered by API when recognizing 
# 3. learn triggered by API during show widgets (x)
# 4. triggered learning during learning (x)
# 5. recognize triggered after learning (x)
# 6. recognize triggered after show widgets (x)        