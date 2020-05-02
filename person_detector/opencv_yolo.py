import numpy as np
import cv2


class OpenCVYolo:
    """
    This class implements the detection pipeline for Darknet Yolov2 and Yolov3. For training of YOLO, you can use
    https://github.com/mmaaz60/darknet repository.
    """

    def __init__(self, classes_file, config_file, weights_file):
        """
        This function loads the Darknet YOLO model using OpenCV DNN module

        :param classes_file: Path to txt file containing the names of all classes of the detection network with
        one name per class in eah line.
        :param config_file: Path to darknet configuration (.cfg) file of the detection network
        :param weights_file: Path to trained weights (.weights) file of the detection network

        :return: None
        """
        # Read the classes file
        with open(classes_file) as f:
            self.classes = [line.strip() for line in f.readlines()]
        # Load the model using OpenCV DNN module
        self.model = cv2.dnn.readNetFromDarknet(config_file, weights_file)
        # Get the model input size from .cfg file
        configurations = OpenCVYolo.get_model_input_size(config_file)
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
        is_person = False  # Flag to indicate if is there any person in the image or not

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
            detection__confidences = out[:, 5:]
            score = np.amax(detection__confidences, axis=1)
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
                    boxes.append([x, y, w, h])
        # Apply non-max suppression to suppress the weak and overlapping bounding boxes
        indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
        bboxes = []
        # Check that if we have any detected bounding box or not
        if len(indices) > 0:
            # Loop over the indices to keep
            for i in indices.flatten():
                x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]  # Extract the bounding box
                confidence = confidences[i]
                bboxes.append([x, y, w, h, confidence])  # Append the bounding box to bboxes

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
