class Homography:
    def __init__(self):
        from cv2 import findHomography as transformation
        self.transformation = transformation

    def calculate_transform(self, src_pts, dst_pts):
        return self.transformation(src_pts, dst_pts)
