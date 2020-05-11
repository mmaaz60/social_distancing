import numpy as np
import cv2


def mouse_handler(event, x, y, flags, data):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(data['image'], (x, y), 3, (0, 0, 255), 5, 16)
        cv2.imshow("Image", data['image'])
        data['points'].append([x, y])


class MarkPoints:
    def __init__(self, image):
        self.image = image
        self.image_with_points_marked = image
        self.num_points = None
        self.data = {}

    def mark_points(self, num_points):
        image_copy = self.image_with_points_marked
        self.data['image'] = image_copy
        self.data['points'] = []

        cv2.setMouseCallback("Image", mouse_handler, self.data)
        cv2.imshow("Image", image_copy)
        cv2.waitKey(0)

        return np.vstack(self.data['points']).astype(float)
