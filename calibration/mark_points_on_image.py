import numpy as np
import cv2


class MarkPoints:
    def __init__(self, image):
        self.image = image
        self.image_with_points_marked = image
        self.num_points = None
        self.data = {}

    def mouse_handler(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.data['image'], (x, y), 3, (0, 0, 255), 5, 16)
            cv2.imshow("Image", self.data['image'])
            self.data['points'].append([x, y])

    def mark_points(self, num_points):
        image_copy = self.image_with_points_marked
        self.data['image'] = image_copy
        self.data['points'] = []

        cv2.setMouseCallback("Image", self.mouse_handler, self.data)
        while True:
            cv2.imshow("Image", image_copy)
            key = cv2.waitKey(1) & 0xFF

            if key == 13 or key == 141:
                break

            if key == 27:
                self.data['points'] = []
                self.data['image'] = self.image

        return np.vstack(self.data['points']).astype(float)
