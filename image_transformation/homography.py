class Homography:
    def __init__(self):
        """
        The function imports findHomography function from OpenCV and assigns it to self.transformation
        """
        from cv2 import findHomography as transform
        self.transform = transform

    def calculate_transform(self, src_pts, dst_pts):
        """
        This function calculates the homography transformation

        :param src_pts: Numpy array of points from source image. Al least 4 points are required. The higher the better.
        :param dst_pts: Numpy array of corresponding points from destination image. The number of points should be same
        as that of the number of point from the source image

        :return: Homography transformation matrix, status mask

        :usage:
        src_pts = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)  # Points from source image
        dst_pts = np.array([[1, 1], [1, 1], [1, 0], [0, 0]], dtype=float)  # Points from destination image
        image_transform = Homography()  # Create class object
        transform_metrics, status = image_transform.calculate_transform(src_pts, dst_pts)  # Calculate transform
        """
        return self.transform(src_pts, dst_pts)
