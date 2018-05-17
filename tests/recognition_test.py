import unittest
from unittest.mock import MagicMock, Mock

from recognition.face_recognizer import FaceRecognizerScheduler, detect_face_from_image
from database.database import SafeSession, User, Picture
from PyQt5.QtCore import QThreadPool


cascade = '/Users/jannik/Desktop/Rasbpi/venv/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_alt.xml'
camera_result_1 = ''

class CameraMock:
    def __init__(self):
        pass


class TestFaceRecognition(unittest.TestCase):

    def set_up_face_recognizer(self, camera,is_learning_callback, finished_learning_callback, user_recognized_callback):
            return FaceRecognizerScheduler(QThreadPool(), camera,cascade, is_learning_callback, finished_learning_callback, user_recognized_callback)

    def test_initial_learn_and_recognize(self):
        def fill_test_db():
            user = User('Username', 'Prename', 'name')
            user2 = User('Jmi', 'John', 'Smith')

            picture1 = Picture()
            picture2 = Picture()

            with SafeSession() as safe_session:
                safe_session.add(user)
                safe_session.add(user2)
                safe_session.commit()

        fill_test_db()

        should_recognize = 'Jmi'

        is_learning_c = Mock()
        finished_learning_c = Mock()
        user_recognized_c = Mock()

        camera = CameraMock()
        camera.capture_face = MagicMock(return_value=camera_result_1)

        f_r_c = self.set_up_face_recognizer(camera, is_learning_c, finished_learning_c, user_recognized_c)

        is_learning_c.assert_called_once()
        finished_learning_c.assert_called_once()
        user_recognized_c.assert_called_with(should_recognize)


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