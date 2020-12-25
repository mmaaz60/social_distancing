import sys
import argparse
from config.config import Configuration as config
import pickle
import numpy as np
import cv2
from person_detector.detector import Detector


def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video_path", required=True, help="Path to video file.")

    return vars(ap.parse_args())


def plot_detections(image, detections):
    for i, det in enumerate(detections):
        x, y, w, h, conf = det
        x, y, w, h = int(x), int(y), int(w), int(h)
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)
    return image


def plot_violations(image, det_points, violations):
    for violation in violations:
        b1, b2 = violation
        p1, p2 = det_points[b1], det_points[b2]
        image = cv2.line(image, tuple(p1), tuple(p2), (0, 0, 255), 2)
    return image


def main():
    # Read program config
    config.load_config("./config.yml")
    # Parse the arguments
    args = parse_arguments()
    video_path = args["video_path"]
    output_video_path = f"{video_path.split('.')[0]}_output.avi"
    # Load the transformation matrix and scale factor from the pkl file
    pkl_file_path = config.cfg["calibration"]["pkl_file_path"]
    with open(pkl_file_path, 'rb') as f:
        transformation_matrix, scale_factor = pickle.load(f)
    # Initialize the person detector
    person_detector = Detector()
    # Read the video
    video = cv2.VideoCapture(video_path)
    w, h = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    # Create the video writer
    video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"MJPG"), fps, (w, h))
    if not video.isOpened():
        print(f"Invalid video path. Existing")
        sys.exit(1)
    # Keep running until video ends
    while True:
        # Read the next frame
        ret, frame = video.read()
        # Break if video ended
        if not ret:
            break
        # Get the person detections
        detections = person_detector.do_inference(frame, 0.5, 0.45)
        # Find out the mid-bottom point of each detection
        det_points = {}
        for i, det in enumerate(detections):
            x, y, w, h, _ = det
            det_points[i] = np.array([int(x + w / 2), int(y + h)])
        # Calculate the distance between bounding boxes
        distances = np.array([[0 for i in range(len(det_points))] for j in range(len(det_points))])
        for i in det_points.keys():
            p1 = det_points[i]
            for j in det_points.keys():
                p2 = det_points[j]
                if i == j:
                    distances[i][j] = 0
                else:
                    dist = np.linalg.norm(p1 - p2)
                    distances[i][j] = dist * scale_factor
        # Check for social distancing violation
        violation_distance_threshold = config.cfg["social_distancing"]["distance_threshold_ft"]
        violations = []
        rows, columns = distances.shape
        for i in range(rows):
            for j in range(columns):
                if not i == j and distances[i][j] < violation_distance_threshold:
                    violations.append([i, j])
        # Plot and display the detections
        frame = plot_detections(frame, detections)
        frame = plot_violations(frame, det_points, violations)
        video_writer.write(frame)
        cv2.imshow("Video Frame", frame)
        cv2.waitKey(10)
    # Release the video and video writer
    video.release()
    video_writer.release()


if __name__ == "__main__":
    main()
