from config.config import Configuration as config
import sys


class Detector:
    def __init__(self):
        if config.cfg["person_detector"]["name"] == "opencv_yolo":
            from person_detector.opencv_yolo import OpenCVYolo as SelectedDetector
        else:
            print(f"The provided detector is not supported. Terminating")
            sys.exit(1)
        self.selected_detector = SelectedDetector(config.cfg["person_detector"]["checkpoint_path"])

    def do_inference(self, image, confidence_threshold, nms_threshold):
        return self.selected_detector.do_inference(image, confidence_threshold, nms_threshold)
