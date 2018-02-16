import threading
import cv2
import numpy as np


class FaceRecognizer():
    def __init__(self):
        self.__lock = threading.Lock()
        self.__face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    def train(self, labels):
        self.__lock.acquire()
        face_recognizer.train(faces, np.array(labels)) 
        self.__lock.release()
    def predict(self):
        self.__lock.acquire()
        label, confidence = face_recognizer.predict(face)
        self.__lock.release()
        return label, confidence
        
        