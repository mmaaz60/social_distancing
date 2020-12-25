import cv2
import numpy as np
from calibration.mark_points_on_image import MarkPoints


class ScaleFactorEstimator:
    def __init__(self, camera_view_image, transformation_matrix):
        self.camera_image = camera_view_image
        self.transformation_metrics = transformation_matrix
        self.camera_view_points = []
        self.top_view_points = []
        self.scale_factor = None

    def mark_points(self, num_points):
        mark_points = MarkPoints(self.camera_image, "Camera View")
        camera_points = mark_points.mark_points(num_points)
        self.camera_view_points.append(camera_points)
        top_view_points = []
        for cam_points in camera_points:
            cam_points = np.append(cam_points, 1)
            points = np.matmul(self.transformation_metrics, cam_points)
            points = points[:2]
            top_view_points.append(points)
        self.top_view_points.append(top_view_points)

    def estimate_scale_factor(self, person_height_ft=6):
        pixel_ditances = []
        for top_view_points_pair in self.top_view_points:
            point_1, point_2 = top_view_points_pair
            pixel_ditances.append(np.linalg.norm(point_1 - point_2))
        pixel_ditances = np.array(pixel_ditances)
        avg_pixel_distance = np.mean(pixel_ditances)
        scale_factor = person_height_ft/avg_pixel_distance

        return scale_factor
