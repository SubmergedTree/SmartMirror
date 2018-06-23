try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    found_picamera_module = True
except:
    found_picamera_module = False
import time
import cv2


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
            print("exception caught")
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
                print("not ret")
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
            self.__camera = CameraCV(cascade, cv2.VideoCapture(0))
        elif which_camera == WhichCamera.PI:
            if found_picamera_module:
                self.__camera = CameraPi(cascade, PiCamera())
            else:
                raise PiCameraNotSupportedException()

    def capture_face(self):
        return self.__camera.capture_face()

    def stop(self):
        print("Camera stop")
        self.__camera.stop = True


#CAMERA_RESOLUTION = (480, 368)
#TODO make attributes private
#TODO close camera or use with

# class Camera():
#     def __init__(self):
#         self.camera = PiCamera()
#         self.camera.resolution = (480, 368)
#         self.camera.framerate = 32
#         self.raw_capture = PiRGBArray(self.camera, (480, 368))
#         time.sleep(0.1) # warm up camera
#     def __get_nearest_face(self, faces):
#         nearest = faces[0]
#         for x in range(1, len(faces)):
#             w_new = faces[x][2]
#             h_new = faces[x][3]
#             w_old = nearest[2]
#             h_old = nearest[3]
#             if (w_new * h_new) > (w_old * h_old):
#                 nearest = faces[x]
#         return nearest
#     def capture_face(self):
#            for frame in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
#                 image = frame.array
#                 gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#                 face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
#                 faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.2, minNeighbors=5);
#                 self.raw_capture.truncate(0)
#                 if len(faces) == 0:
#                     continue
#                 else:
#                     (x,y,w,h) = self.__get_nearest_face(faces)
#                     return gray_image[y:y+w, x:x+h]
#
# # For testing
# cam = Camera()
# image = cam.capture_face()
#
# cv2.imshow("Image", image)
# cv2.waitKey(0)
