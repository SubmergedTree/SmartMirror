import unittest
import cv2
from recognition.camera import CameraCV, WhichCamera, Camera
from root_dir import ROOT_DIR

cascade = ROOT_DIR + "/util/lbpcascade_frontalface.xml"

image_1_person = cv2.imread('test_data/faces/subject02.wink.pgm')


class CV2Mock:
    def __init__(self, ret_val):
        self.ret_val = ret_val

    def read(self):
        return True, self.ret_val

    def release(self):
        pass


class CameraTest(unittest.TestCase):

    def test_camera_cv(self):
        camera = CameraCV(cascade, CV2Mock(image_1_person))
        face = camera.capture_face()
        cv2.imwrite('testimage.png', face)
        self.assertIsNotNone(face)

    #def test_cv(self):
    #    camera = Camera(cascade, WhichCamera.CV)
    #    face = camera.capture_face()
    #    cv2.imwrite("test.png", face)
    #    self.assertIsNotNone(face)