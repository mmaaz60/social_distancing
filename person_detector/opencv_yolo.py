import numpy as np
import cv2


class OpenCVYolo:
    """
    This class implements the detection pipeline for Darknet Yolov2 and Yolov3. For training of YOLO, you can use
    https://github.com/mmaaz60/darknet repository.
    """
    def __init__(self, classes, config, weights):
        """
        This function loads the Darknet YOLO model using OpenCV DNN module

        :param classes: A txt file containing the names of all classes of the detection network with
        one name per class in eah line.
        :param config: Darknet configuration (.cfg) file of the detection network
        :param weights: Trained weights (.weights) file of the detection network

        :return: None
        """
        pass

    def do_inference(self, image, nms_threshold, confidence_threshold):
        """
        This function does inference on the image passed and return the person bounding boxes

        :param image: A BGR numpy array (the result of cv2.imread() or cv2.VideoCapture())
        :param nms_threshold: Non Maximal Threshold for YOLO object detector
        :param confidence_threshold: Minimum confidence threshold below which all boxes should be discarded
        :return:
        """
        pass
