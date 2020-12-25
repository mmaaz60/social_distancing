import cv2
import numpy as np
from calibration.mark_points_on_image import MarkPoints
from image_transformation.transform import Transform


class TransformCameraView:
    def __init__(self, camera_view_image):
        self.camera_image = cv2.resize(camera_view_image, (640, 360))
        self.top_view_size = (360, 360, 3)
        self.top_view = np.zeros(self.top_view_size, np.uint8)
        self.camera_view_points = None
        self.top_view_points = None
        self.transformation_metrics = None
        self.transformed_image = None

    def mark_points_on_camera_view_image(self, num_points):
        mark_points = MarkPoints(self.camera_image, "Camera View")
        self.camera_view_points = mark_points.mark_points(num_points)

    def mark_points_on_top_view(self, num_points):
        mark_points = MarkPoints(self.top_view, "Top View")
        self.top_view_points = mark_points.mark_points(num_points)

    def calculate_transformation(self):
        transform = Transform()
        transformation = transform.calculate_transform(self.camera_view_points, self.top_view_points)
        self.transformation_metrics = transformation[0]

    def generate_transformed_image(self):
        self.transformed_image = cv2.warpPerspective(self.camera_image, self.transformation_metrics,
                                                     self.top_view_size[0:2])

    def display_camera_image_on_top_view(self):
        cv2.imshow("Transformed Image", self.transformed_image)
        cv2.waitKey(0)
