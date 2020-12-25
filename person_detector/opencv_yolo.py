import numpy as np
import cv2


class OpenCVYolo:
    """
    This class implements the detection pipeline for Darknet Yolov2 and Yolov3. For training of YOLO, you can use
    https://github.com/mmaaz60/darknet repository.
    """

    def __init__(self, checkpoint_path):
        """
        This function loads the Darknet YOLO model using OpenCV DNN module

        :param checkpoint_path: Path to the checkpoints directory. In case of OpenCV Yolo, checkpoints directory must
        contains a three files, classed.txt, yolo.cfg, yolo.weights.
        :classes.txt: File containing the names of all classes of the network with one class name per line of file.
        :yolo.cfg: Darknet configuration (.cfg) file of the Yolo detection network
        :yolo.weights: Darknet trained weights (.weights) file of the Yolo detection network

        :return: None
        """
        # Read the classes file
        with open(f"{checkpoint_path}/classes.txt") as f:
            self.classes = [line.strip() for line in f.readlines()]
        # Load the model using OpenCV DNN module
        self.model = cv2.dnn.readNetFromDarknet(f"{checkpoint_path}/yolo.cfg", f"{checkpoint_path}/yolo.weights")
        # Get the model input size from .cfg file
        configurations = OpenCVYolo.get_model_input_size(f"{checkpoint_path}/yolo.cfg")
        self.width, self.height = int(configurations["width"]), int(configurations["height"])
        # Get the model's output layers
        layer_names = self.model.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1] for i in self.model.getUnconnectedOutLayers()]

    def do_inference(self, image, confidence_threshold, nms_threshold):
        """
        This function does inference on the image passed and return the person bounding boxes

        :param image: A BGR numpy array (i.e. the result of cv2.imread() or read() call after cv2.VideoCapture())
        :param nms_threshold: Non Maximal Threshold for YOLO object detector
        :param confidence_threshold: Minimum confidence threshold below which all boxes should be discarded

        :return: List of person bounding boxes ([[x, y, w, h, confidence], ...])
        """

        h, w, _ = image.shape  # Get the input image shape
        # Create input blob
        blob = cv2.dnn.blobFromImage(image=image, scalefactor=1 / 255,
                                     size=(self.width, self.height), mean=(0, 0, 0), swapRB=True, crop=False)
        # Det input blob for the network
        self.model.setInput(blob)
        # Run inference through the network
        outs = self.model.forward(self.output_layers)
        # Initialize some lists for detected class ids, confidences and boxes
        class_ids = []
        confidences = []
        boxes = []
        # Iterate through outputs and append person bounding boxes into boxes
        for out in outs:
            detection_confidences = out[:, 5:]
            score = np.amax(detection_confidences, axis=1)
            out_mask = [score > confidence_threshold]
            out = out[tuple(out_mask)]
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # Scale the bounding box back relative to the size of the image
                center_x, center_y, width, height = detection[0:4] * np.array([w, h, w, h])
                # Get the top-left corner of the bounding box
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))

                # Check if classified box is person
                if self.classes[class_id] == "person":
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, width, height])
        # Apply non-max suppression to suppress the weak and overlapping bounding boxes
        indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
        bboxes = []
        # Check that if we have any detected bounding box or not
        if len(indices) > 0:
            # Loop over the indices to keep
            for i in indices.flatten():
                x, y, width, height = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]  # Extract the bounding box
                confidence = confidences[i]
                bboxes.append([x, y, width, height, confidence])  # Append the bounding box to bboxes

        return bboxes

    @staticmethod
    def get_model_input_size(config_file):
        config = {}
        with open(config_file, "r") as cfg:
            configurations = cfg.read().split("\n")
            for configuration in configurations:
                config_option = configuration.split('=')
                if len(config_option) == 2:
                    config[config_option[0]] = config_option[1]
        return config
