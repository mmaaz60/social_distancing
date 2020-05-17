import numpy as np
import cv2
import sys


class MarkPoints:
    def __init__(self, image, image_name):
        self.image_name = image_name
        self.image = image
        self.num_points = None
        self.data = {}

    def mouse_handler(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.data['points'].append([x, y])
            self.data['image'] = self.image.copy()
            for points in self.data['points']:
                cv2.circle(self.data['image'], (points[0], points[1]), 3, (0, 0, 255), 5, 16)
            if len(self.data['points']) > self.data['required_points']:
                cv2.putText(self.data['image'], f"You have drawn more than {self.data['required_points']} points. Press ESC to restart drawing.",
                            (1, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)
            cv2.imshow(f"{self.image_name}", self.data['image'])

    def mark_points(self, num_points):
        cv2.imshow(f"{self.image_name}", self.image)

        self.data['image'] = self.image.copy()
        self.data['points'] = []
        self.data['required_points'] = num_points

        cv2.setMouseCallback(f"{self.image_name}", self.mouse_handler, self.data)
        while True:
            cv2.imshow(f"{self.image_name}", self.data['image'])
            key = cv2.waitKey(1) & 0xFF

            if key == 13 or key == 141:
                if len(self.data['points']) == num_points:
                    break
                else:
                    cv2.putText(self.data['image'], f"You have not drawn {num_points} yet. Please draw at least {num_points} and then press ENTER",
                                (1, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.imshow(f"{self.image_name}", self.data['image'])

            if len(self.data['points']) == num_points:
                cv2.putText(self.data['image'], f"You have drawn {num_points} points. Press ENTER to save or ESC to redraw.",
                            (1, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2)
                cv2.imshow(f"{self.image_name}", self.data['image'])
                key = cv2.waitKey(0)
                if key == 13 or key == 141:
                    break
                elif key == 27:
                    self.data['points'] = []
                    self.data['image'] = self.image.copy()
                else:
                    self.data['image'] = self.image.copy()
                    cv2.putText(self.data['image'], f"You have entered invalid key. Terminating in 5 seconds!",
                                (1, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.imshow(f"{self.image_name}", self.data['image'])
                    key = cv2.waitKey(5000)
                    sys.exit(1)

            if key == 27:
                self.data['points'] = []
                self.data['image'] = self.image.copy()

        return np.vstack(self.data['points']).astype(float)
