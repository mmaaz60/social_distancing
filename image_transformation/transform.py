from config.config import Configuration as config
import sys


class Transform:
    def __init__(self):
        if config.cfg["calibration"]["image_transformation"] == "homography":
            from image_transformation.homography import Homography as Transformation
        else:
            print(f"The requested transformation is not supported. Terminating")
            sys.exit(1)
        self.transform = Transformation()

    def calculate_transform(self, src_pts, dst_pts):
        return self.transform.calculate_transform(src_pts, dst_pts)
