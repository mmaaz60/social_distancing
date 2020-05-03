from config.config import Configuration as config
import sys


class Detector:
    def __init__(self):
        if config.cfg["image_transformation"] == "homography":
            from image_transformation.homography import Homography as Transformation
        else:
            print(f"The requested transformation is not supported. Terminating")
            sys.exit(1)
        self.transform = Transformation()

    def do_inference(self, src_pts, dst_pts):
        return self.transform.calculate_transform(src_pts, dst_pts)
