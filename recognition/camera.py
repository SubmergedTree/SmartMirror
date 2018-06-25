try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    found_picamera_module = True
except:
    found_picamera_module = False
import time
import cv2
from util.logger import Logger

SCALE_FACTOR = 1.2
MIN_NEIGHBORS = 5


class PiCameraNotSupportedException(Exception):
    pass


class WhichCamera:
    PI = 0
    CV = 1


class BaseCamera:
    def __int__(self, cascade):
        self.__cascade = cascade
        self._faces = []
        self._gray_image = None
        self.stop = False

    def _get_nearest_face(self):
        nearest = self._faces[0]
        for x in range(1, len(self._faces)):
            w_new = self._faces[x][2]
            h_new = self._faces[x][3]
            w_old = nearest[2]
            h_old = nearest[3]
            if (w_new * h_new) > (w_old * h_old):
                nearest = self._faces[x]
        (x, y, w, h) = nearest
        return self._gray_image[y:y+w, x:x+h]

    def _detect_faces(self, frame):
        try:
            self._gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(self.__cascade)
            self._faces = face_cascade.detectMultiScale(self._gray_image, scaleFactor=SCALE_FACTOR, minNeighbors=MIN_NEIGHBORS)
        except cv2.error:
            Logger.error("Exception caught in _detect_faces in BaseCamera.")
            pass

class CameraPi(BaseCamera):
    def __init__(self, cascade, pi_camera):
        super(CameraPi, self).__int__(cascade)
        self.__camera = pi_camera
        self.__camera.resolution = (480, 368)
        self.__camera.framerate = 32
        self.__raw_capture = PiRGBArray(self.__camera, (480, 368))
        time.sleep(0.1)  # warm up camera

    def capture_face(self):
        for frame in self.__camera.capture_continuous(self.__raw_capture, format="bgr", use_video_port=True):
            self._detect_faces(frame.array)
            self.__raw_capture.truncate(0)
            if self.stop:
                return None
            elif len(self._faces) == 0:
                continue
            else:
                return self._get_nearest_face()


class CameraCV(BaseCamera):
    def __init__(self, cascade, capture_device):
        super(CameraCV, self).__int__(cascade)
        self.__capture_device = capture_device

    def capture_face(self):
        while not self.stop:
            ret, frame = self.__capture_device.read()
            if not ret:
                Logger.warn("Reading from CV Camera failed. Rebuild capture device and retry")
                self.__capture_device = cv2.VideoCapture(0)  # dirty hack to reset camera when an error occurred
                continue
            self._detect_faces(frame)
            if len(self._faces) == 0:
                continue
            else:
                self.__capture_device.release()
                return self._get_nearest_face()
        return None


class Camera:
    def __init__(self, cascade, which_camera):
        global found_picamera_module
        if which_camera == WhichCamera.CV:
            Logger.info("using cv camera")
            self.__camera = CameraCV(cascade, cv2.VideoCapture(0))
        elif which_camera == WhichCamera.PI:
            if found_picamera_module:
                Logger.info("using pi camera")
                self.__camera = CameraPi(cascade, PiCamera())
            else:
                Logger.error("attempt to use pi camera but it is not supported on this device " +
                           "or the library is not installed")
                raise PiCameraNotSupportedException()

    def capture_face(self):
        return self.__camera.capture_face()

    def stop(self):
        pass # QUESTION: does this break PiCamera ?
        # print("Camera stop")
        #self.__camera.stop = True # stopping camera chrashes the whole appplication.

