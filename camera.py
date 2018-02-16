from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#CAMERA_RESOLUTION = (480, 368)
#TODO make attributes private
class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (480, 368)
        self.camera.framerate = 32
        self.raw_capture = PiRGBArray(self.camera, (480, 368))
        time.sleep(0.1) # warm up camera
    def __get_nearest_face(self, faces):
        nearest = faces[0]
        for x in range(1, len(faces)):
            w_new = faces[x][2]
            h_new = faces[x][3]
            w_old = nearest[2]
            h_old = nearest[3]
            if (w_new * h_new) > (w_old * h_old):
                nearest = faces[x]
        return nearest
    def capture_face(self):
           for frame in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
                image = frame.array
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
                faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.2, minNeighbors=5);
                self.raw_capture.truncate(0) 
                if len(faces) == 0:
                    continue
                else:
                    (x,y,w,h) = self.__get_nearest_face(faces)
                    return gray_image[y:y+w, x:x+h]

# For testing
#cam = Camera()
#image = cam.capture_face()

#cv2.imshow("Image", image)
#cv2.waitKey(0)
