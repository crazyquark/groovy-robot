import picamera
from picamera.array import PiRGBArray

import time
import numpy as np

import cv2

from .camera import Camera


class PiCamera(Camera):
    '''
        Class for using a Pi Camera
        Inspired from https://github.com/miguelgrinberg/flask-video-streaming/blob/master/camera_pi.py
    '''

    def __init__(self):
        super(PiCamera, self).__init__()

        self.camera = None

        # Create stream
        self.stream = cv2.VideoCapture(0)

        # self.stream.set(cv2.CAP_PROP_FPS, 25)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # self.load_model()

    def load_model(self):
        # based on: https://github.com/djmv/MobilNet_SSD_opencv
        # MIT License
        self.cv_classnames = {0: 'background',
                              1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
                              5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
                              10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
                              14: 'motorbike', 15: 'person', 16: 'pottedplant',
                              17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}

        self.net = cv2.dnn.readNetFromCaffe(
            'cv/MobileNetSSD_deploy.prototxt', 'cv/MobileNetSSD_deploy.caffemodel')

        # Based on https://github.com/shantnu/FaceDetect/blob/master/face_detect_cv3.py
        self.faces_detector = cv2.CascadeClassifier(
            'cv/haarcascade_frontalface_default.xml')

    def process_frame(self, frame, detect):
        '''
            Process frame with OpenCV
        '''
        image = cv2.flip(frame, -1)

        if detect:
            self.detect_faces(image)
        
        # print FPS on image
        cv2.putText(image, str(self.fps), (0, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        result = cv2.imencode('.jpg', image)
        data = np.array(result[1], dtype=np.uint8).tostring()

        return data

    def detect_faces(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = self.faces_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    def mobile_net_detect(self, image):
        # MobileNet requires fixed dimensions for input image(s)
        # so we have to ensure that it is resized to 300x300 pixels.
        # set a scale factor to image because network the objects has differents size.
        # We perform a mean subtraction (127.5, 127.5, 127.5) to normalize the input;
        # after executing this command our "blob" now has the shape:
        # (1, 3, 300, 300)
        frame_resized = cv2.resize(image, (300, 300))

        blob = cv2.dnn.blobFromImage(
            frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        # Set to network the input blob
        self.net.setInput(blob)
        # Prediction of network
        detections = self.net.forward()

        # Size of frame resize (300x300)
        cols = frame_resized.shape[1]
        rows = frame_resized.shape[0]

        # For get the class and location of object detected,
        # There is a fix index for class, location and confidence
        # value in @detections array .
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]  # Confidence of prediction
            if confidence > 0.2:  # Filter prediction
                class_id = int(detections[0, 0, i, 1])  # Class label

                # Object location
                xLeftBottom = int(detections[0, 0, i, 3] * cols)
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop = int(detections[0, 0, i, 5] * cols)
                yRightTop = int(detections[0, 0, i, 6] * rows)

                # Factor for scale to original size of image
                heightFactor = image.shape[0]/300.0
                widthFactor = image.shape[1]/300.0
                # Scale object detection to image
                xLeftBottom = int(widthFactor * xLeftBottom)
                yLeftBottom = int(heightFactor * yLeftBottom)
                xRightTop = int(widthFactor * xRightTop)
                yRightTop = int(heightFactor * yRightTop)
                # Draw location of object
                cv2.rectangle(image, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                              (0, 255, 0))

                # Draw label and confidence of prediction in image resized
                if class_id in self.cv_classnames:
                    label = self.cv_classnames[class_id] + \
                        ": " + str(confidence)
                    labelSize, baseLine = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv2.rectangle(image, (xLeftBottom, yLeftBottom - labelSize[1]),
                                  (xLeftBottom +
                                   labelSize[0], yLeftBottom + baseLine),
                                  (255, 255, 255), cv2.FILLED)
                    cv2.putText(image, label, (xLeftBottom, yLeftBottom),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    def get_frame(self):
        '''
            Get current camera frame
        '''
        if self.frame:
            return self.frame

    def halt(self):
        '''
            Release camera
        '''
        if self.stream:
            self.stream.release()
