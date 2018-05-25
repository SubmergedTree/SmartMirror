import unittest
from unittest.mock import MagicMock, Mock

from recognition.TO_REMOVE_face_recognizer import FaceRecognizerScheduler, detect_face_from_image
from database.database import SafeSession, User, Picture
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QApplication
import sys


import cv2

# TODO: test data need to be included in the remote git repository. Without them no test would pass
# TODO: find solution for exposing full path which is also not valid in other environments.


cascade = '/Users/jannik/PycharmProjects/SmartMirror/util/lbpcascade_frontalface.xml'
camera_result_1 = detect_face_from_image(cv2.imread('test_data/faces/subject02.noglasses.pgm'), cascade)

user = User(username='Username', prename='Prename', name='name')
user2 = User(username='Jmi', prename='John', name='Smith')

picture1_user1 = Picture(username=user.username, image_path='test_data/faces/subject01.centerlight.pgm')
picture2_user1 = Picture(username=user.username, image_path='test_data/faces/subject01.glasses.pgm')

picture1_user2 = Picture(username=user2.username, image_path='test_data/faces/subject02.centerlight.pgm')
picture2_user2 = Picture(username=user2.username, image_path='test_data/faces/subject02.glasses.pgm')
picture3_user2 = Picture(username=user2.username, image_path='test_data/faces/subject02.happy.pgm')


class TestFaceRecognition(unittest.TestCase):

    def set_up_face_recognizer(self, camera,is_learning_callback, finished_learning_callback, user_recognized_callback, user_dao, picture_dao):
        return FaceRecognizerScheduler(QThreadPool(), camera,cascade, is_learning_callback,
                                           finished_learning_callback, user_recognized_callback, user_dao, picture_dao)

    def test_initial_learn_and_recognize(self):
        app = QApplication([])
        def picture_dao_get_paths_by_username(username):
            if username == user.username:
                return [picture1_user1, picture2_user1]
            elif username == user2.username:
                return [picture1_user2, picture2_user2, picture3_user2]
            return []

        should_recognize = 'Jmi'

        is_learning_c = Mock()
        finished_learning_c = Mock()
        user_recognized_c = Mock()

        camera = MagicMock()
        camera.capture_face = MagicMock(return_value=camera_result_1)

        user_dao = MagicMock()
        user_dao.get_all_user = MagicMock(return_value=[user, user2])

        picture_dao = MagicMock()
        picture_dao.get_paths_by_username = MagicMock(side_effect=picture_dao_get_paths_by_username)

        f_r_c = self.set_up_face_recognizer(camera, is_learning_c, finished_learning_c,
                                            user_recognized_c, user_dao, picture_dao)
        is_learning_c.assert_called_once()
        finished_learning_c.assert_called_once()
        user_recognized_c.assert_called_with(should_recognize)
        sys.exit(app.exec_())



    def test_initial_learn_and_recognize_with_user_without_pictures(self):
        pass

    def test_interrupt_recognition_with_learning(self):
        pass

    def test_learn_triggered_during_show_widgets(self):
        pass

    def test_trigger_learning_during_learningn(self):
        pass

    def test_recognize_triggered_during_learning(self):
        pass

    def test_recognize_triggered_during_learning(self):
        pass