from recognition.recognition import Scheduler, detect_face_from_image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from database.database import *
import sys
import cv2


cascade = '/Users/jannik/PycharmProjects/SmartMirror/util/lbpcascade_frontalface.xml'
camera_result_1_gray, camera_result_1_faces = detect_face_from_image(cv2.imread('test_data/faces/subject02.wink.pgm'), cascade)
camera_result_2_gray, camera_result_2_faces = detect_face_from_image(cv2.imread('test_data/faces/subject03.sad.pgm'), cascade)


user = User(username='Username', prename='Prename', name='name')
user2 = User(username='Jmi', prename='John', name='Smith')

picture1_user1 = Picture(username=user.username, image_path='test_data/faces/subject01.centerlight.pgm')
picture2_user1 = Picture(username=user.username, image_path='test_data/faces/subject01.glasses.pgm')
picture3_user1 = Picture(username=user.username, image_path='test_data/faces/subject01.happy.pgm')
picture4_user1 = Picture(username=user.username, image_path='test_data/faces/subject01.leftlight.pgm')
picture5_user1 = Picture(username=user.username, image_path='test_data/faces/subject01.noglasses.pgm')

picture1_user2 = Picture(username=user2.username, image_path='test_data/faces/subject02.centerlight.pgm')
picture2_user2 = Picture(username=user2.username, image_path='test_data/faces/subject02.glasses.pgm')
picture3_user2 = Picture(username=user2.username, image_path='test_data/faces/subject02.happy.pgm')
picture4_user2 = Picture(username=user2.username, image_path='test_data/faces/subject02.leftlight.pgm')
picture5_user2 = Picture(username=user2.username, image_path='test_data/faces/subject02.noglasses.pgm')


class UserDaoMock:
    def get_all_user(self):
        return [user, user2]


class PictureDaoMock:
    def get_paths_by_username(self, username):
        if username == user.username:
            return [picture1_user1, picture2_user1, picture3_user1, picture4_user1, picture5_user1]
        elif username == user2.username:
            return [picture1_user2, picture2_user2, picture3_user2, picture4_user2, picture5_user2]
        return []


class CameraMock:
    def __init__(self):
        pass

    def capture_face(self):
        return camera_result_1_gray


class CameraMockUnknownFace:
    def __init__(self):
        pass

    def capture_face(self):
        return camera_result_2_gray


#### Test ####

results = {'test_learn_recognize': 'failed',
           'test_learn_recognize_learn_recognize': 'failed',
           'test_learn_recognize_recognize': 'failed',
           'test_learn_learn_recognize': 'failed'}

s = None
s2 = None
s3 = None
s4 = None
s5 = None

test_try_to_recognize_unknown_face_user_recognized = None


def eval_test_try_to_recognize_unknown_face():
    if test_try_to_recognize_unknown_face_user_recognized == False:
        results['test_learn_learn_recognize'] = 'success'


def test_learn_recognize():
    global s
    to_recognize = 'Jmi'

    cb1 = False
    cb2 = False

    def is_learning_cb():
        nonlocal cb1
        cb1 = True

    def finished_learning_cb():
        nonlocal cb2
        cb2 = True

    def user_recognized_cb(username):
        if username == to_recognize:
            if cb1 and cb2:
                results['test_learn_recognize'] = 'success'

    s = Scheduler(UserDaoMock(), PictureDaoMock(),CameraMock(),cascade, is_learning_cb, finished_learning_cb, user_recognized_cb)


def test_learn_recognize_learn_recognize():
    global s2
    to_recognize = 'Jmi'

    cb1_1 = False
    cb2_1 = False

    cb1_2 = False
    cb2_2 = False

    cb1_3 = False
    cb2_3 = False

    def is_learning_cb():
        nonlocal cb1_1, cb2_1
        #print("TEST2: IS LEARNING")
        if not cb1_1:
            cb1_1 = True
        else:
            cb2_1 = True

    def finished_learning_cb():
        nonlocal cb1_2, cb2_2
        #print("TEST2: FINISHED LEARNING")
        if not cb1_2:
            cb1_2 = True
        else:
            cb2_2 = True

    def user_recognized_cb(username):
        nonlocal cb1_3, cb2_3
        #print(username)
        if username == to_recognize:
            if not cb1_3:
                cb1_3 = True
                s2.learn()
            else:
                cb2_3 = True
                if cb1_1 and cb1_2 and cb1_3 and cb2_1 and cb2_2 and cb2_3 and cb1_3 and cb2_3:
                    results['test_learn_recognize_learn_recognize'] = 'success'

    s2 = Scheduler(UserDaoMock(), PictureDaoMock(),CameraMock(),cascade, is_learning_cb, finished_learning_cb, user_recognized_cb)


def test_learn_recognize_recognize():
    global s3
    to_recognize = 'Jmi'

    cb1_1 = False
    cb2_1 = False

    cb1_2 = False
    cb2_2 = False

    cb1_3 = False
    cb2_3 = False


    def is_learning_cb():
        nonlocal cb1_1, cb2_1
        # print("TEST2: IS LEARNING")
        if not cb1_1:
            cb1_1 = True
        else:
            cb2_1 = True


    def finished_learning_cb():
        nonlocal cb1_2, cb2_2
        # print("TEST2: FINISHED LEARNING")
        if not cb1_2:
            cb1_2 = True
        else:
            cb2_2 = True

    def user_recognized_cb(username):
        nonlocal cb1_3, cb2_3
        if username == to_recognize:
            if not cb1_3:
                cb1_3 = True
                s3.schedule()
            else:
                cb2_3 = True
                if cb1_1 and cb1_2 and cb1_3 and not cb2_1 and not cb2_2 and cb2_3 and cb1_3 and cb2_3:
                    results['test_learn_recognize_recognize'] = 'success'


    s3 = Scheduler(UserDaoMock(), PictureDaoMock(),CameraMock(),cascade, is_learning_cb, finished_learning_cb, user_recognized_cb)


def test_learn_learn_recognize():  # TODO
    global s4
    to_recognize = 'Jmi'

    cb1_1 = False
    cb2_1 = False

    cb1_2 = False
    cb2_2 = False

    cb1_3 = False
    cb2_3 = False


    def is_learning_cb():
        nonlocal cb1_1, cb2_1
        # print("TEST2: IS LEARNING")
        if not cb1_1:
            cb1_1 = True
        else:
            cb2_1 = True


    def finished_learning_cb():
        nonlocal cb1_2, cb2_2
        # print("TEST2: FINISHED LEARNING")
        if not cb1_2:
            cb1_2 = True
        else:
            cb2_2 = True

    def user_recognized_cb(username):
        nonlocal cb1_3, cb2_3
        if username == to_recognize:
            if not cb1_3:
                cb1_3 = True
                s3.schedule()
            else:
                cb2_3 = True
                if cb1_1 and cb1_2 and cb1_3 and not cb2_1 and not cb2_2 and cb2_3 and cb1_3 and cb2_3:
                    pass
                    #results['test_learn_recognize_recognize'] = 'success'


    s4 = Scheduler(UserDaoMock(), PictureDaoMock(),CameraMock(),cascade, is_learning_cb, finished_learning_cb, user_recognized_cb)


def test_try_to_recognize_unknown_face():
    global s5

    def is_learning_cb():
        pass

    def finished_learning_cb():
        global test_try_to_recognize_unknown_face_user_recognized
        test_try_to_recognize_unknown_face_user_recognized = False

    def user_recognized_cb(username):
        global test_try_to_recognize_unknown_face_user_recognized
        test_try_to_recognize_unknown_face_user_recognized = True

    s5 = Scheduler(UserDaoMock(), PictureDaoMock(),CameraMockUnknownFace(),cascade, is_learning_cb, finished_learning_cb, user_recognized_cb)



#### End Tests ####


class TestWindow(QMainWindow):
    def __init__(self):
        super(TestWindow, self).__init__()
        layout = QVBoxLayout()
        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        test_learn_recognize()
        test_learn_recognize_learn_recognize()
        test_learn_recognize_recognize()
        test_try_to_recognize_unknown_face()
        self.show()


def on_quit():
    eval_test_try_to_recognize_unknown_face()
    for key, value in results.items():
        print(key + ": " + value)
    print("quit")

app = QApplication([])
t = TestWindow()
print("INSTRUCTION: Wait until test finished.")
timer = QTimer()
timer.timeout.connect(lambda: t.close())
timer.setSingleShot(True)
timer.start(900)

app.aboutToQuit.connect(on_quit)
sys.exit(app.exec_())
