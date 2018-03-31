import cv2
import os
import numpy as np
from cmath import rect

import threading

import camera
import shared
import database

class Learner():
    def __init__(self,face_recognizer, train_new_picture, username = None, img_path):
        self.__train_new = train_new_picture
        self.__face_recognizer = face_recognizer
        self.__username = username
        self.__img_path = img_path
    def run(self):
        self.__fetch_data()
        self.__train()
    def __fetch_data(self):
        with database.DatabaseAccess() as db:
            if self.train_new_picture is True:
                camera = camera.Camera()
                gray_img = camera.capture_face()
                #img_name =     
                cv2.imwrite(os.path.join(self.__img_path , 'waka.jpg'),gray_img)
               # db.insert_picture((self.__username,PATH))
    def __train(self):
        pass