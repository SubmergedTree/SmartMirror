import unittest
from unittest.mock import MagicMock

from recognition.face_recognizer import FaceRecognizerScheduler
from PyQt5.QtCore import QThreadPool

cascade = ''
camera_result_1 = ''

class CameraMock:
    def __init__(self):
        pass


class TestFaceRecognition(unittest.TestCase):

    def set_up_face_recognizer(self, camera,is_learning_callback, finished_learning_callback, user_recognized_callback):
            return FaceRecognizerScheduler(QThreadPool(), camera,cascade, is_learning_callback, finished_learning_callback, user_recognized_callback)

    def test_initial_learn_and_recognize(self):

        def is_learning_c():
            pass

        def finished_learning_c():
            pass

        def user_recognized_c(username):
            pass

        camera = CameraMock()
        camera.capture_face = MagicMock(return_value=camera_result_1)

        f_r_c = self.set_up_face_recognizer(camera, is_learning_c, finished_learning_c(), user_recognized_c())

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