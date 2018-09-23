try:
    import picamera
    from picamera.array import PiRGBArray
    RUNNING_ON_PI = True
except ImportError:
    RUNNING_ON_PI = False

from threading import Thread
import time
import cv2
import numpy as np


class CameraServer(Thread):
    '''
        An autostart camera thread that continously captures images from the camera for processing
        Inspired from https://github.com/crazyquark/flask-video-streaming/blob/master/camera_pi.py
    '''

    def __init__(self):
        Thread.__init__(self)

        self.resolution = (800, 600)
        self.running = True

        self.camera = None

        if RUNNING_ON_PI:
            # Camera setup
            self.camera = picamera.PiCamera()

            # Create stream
            self.stream = PiRGBArray(self.camera)

            # Let camera warm up (??)
            self.camera.start_preview()
            time.sleep(2)

            self.camera.resolution = (800, 600)
            self.camera.framerate = 25
            self.camera.hflip = True
            self.camera.vflip = True

        self.frame = None
        self.dummy_frame()

        self.load_model()

        self.start()

    def dummy_frame(self):
        '''
            If not on RPi return a dummy frame
        '''
        if not hasattr(self, 'frame'):
            with open('./r_server/static/wall-e-800.jpg', 'rb') as image:
                self.frame = image.read()

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

    def run(self):
        if not RUNNING_ON_PI:
            return

        for frame in self.camera.capture_continuous(self.stream, format='bgr', use_video_port=True):
            # Stop thread
            if not self.running:
                return

            # Store frame
            self.frame = frame

            # reset stream for next frame
            self.stream.truncate(0)

    def process_frame(self, frame):
        '''
            Process frame with OpenCV
        '''
        image = frame.array

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
                    label = self.cv_classnames[class_id] + ": " + str(confidence)
                    labelSize, baseLine = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv2.rectangle(image, (xLeftBottom, yLeftBottom - labelSize[1]),
                                        (xLeftBottom +
                                        labelSize[0], yLeftBottom + baseLine),
                                        (255, 255, 255), cv2.FILLED)
                    cv2.putText(image, label, (xLeftBottom, yLeftBottom),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        result = cv2.imencode('.jpg', image)
        data = np.array(result[1], dtype=np.uint8).tostring()

        return data

    def get_frame(self):
        '''
            Get current camera frame
        '''
        return self.process_frame(self.frame)

    def halt(self):
        '''
            Stop server thread
        '''
        self.running = False
        if self.camera:
            self.camera.close()
            self.stream.close()
