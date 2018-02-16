import cv2
import os
import numpy as np
from cmath import rect

import threading

import camera
import shared

class Learner():
    def __init__(self,face_recognizer, train_new_picture):
        self.__train_new = train_new_picture
        self.__face_recognizer = face_recognizer
    def run(self):
        self.__fetch_data()
        self.__train()
    def __fetch_data(self):
        pass
    def __train(self):
        pass