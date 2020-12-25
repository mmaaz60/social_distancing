import sys
import argparse
import cv2
from config.config import Configuration
from calibration.transform_camera_view import TransformCameraView


def calibrate():
    pass


def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video_path", required=False, help="Path to video file.",
                    default="/home/maaz/PycharmProjects/social_distancing/data/AVG-TownCentre-raw.webm")
    ap.add_argument("-n", "--num_points", required=False, type=int, default=4, help="Number of calibration points.")

    return vars(ap.parse_args())


if __name__ == "__main__":
    # Read program config
    Configuration.load_config("./config.yml")
    # Parse the command line arguments
    args = parse_arguments()
    video_path = args["video_path"]
    num_points = args["num_points"]
    # Read video and get the first frame
    video = cv2.VideoCapture(video_path)
    if video.isOpened():
        ret, frame = video.read()
        if not ret:
            print(f"Error reading the video file. Existing")
            sys.exit(1)
    else:
        print(f"Invalid video path. Existing")
        sys.exit(1)
    video.release()
    # Calibrate using TransformCameraView class
    calibrator = TransformCameraView(frame)
    calibrator.mark_points_on_camera_view_image(num_points)
    calibrator.mark_points_on_top_view(num_points)
    calibrator.calculate_transformation()
    calibrator.generate_transformed_image()
    calibrator.display_camera_image_on_top_view()
