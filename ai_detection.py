import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

class AIDetectionFrame(ttk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master, padding="20")
        self.return_callback = return_callback
        self.master = master

        self.create_widgets()
        self.load_model()

    def create_widgets(self):
        ttk.Label(self, text="AI-based Human Edge Detection", font=("Arial", 16)).pack(pady=20)

        self.load_button = ttk.Button(self, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        self.detect_button = ttk.Button(self, text="Detect Humans", command=self.detect_humans)
        self.detect_button.pack(pady=10)

        self.image_frame = ttk.Frame(self)
        self.image_frame.pack(pady=10)

        self.original_image_label = ttk.Label(self.image_frame)
        self.original_image_label.pack(side=tk.LEFT, padx=10)

        self.detected_image_label = ttk.Label(self.image_frame)
        self.detected_image_label.pack(side=tk.RIGHT, padx=10)

        ttk.Button(self, text="Back to Main", command=self.return_to_main).pack(pady=10)

    def load_model(self):
        # Load the model
        model_handle = "https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"
        self.model = hub.load(model_handle)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((400, 400))
            self.photo = ImageTk.PhotoImage(self.image)
            self.original_image_label.config(image=self.photo)
            self.original_image_label.image = self.photo

    def detect_humans(self):
        if not hasattr(self, 'image'):
            messagebox.showerror("Error", "Please load an image first.")
            return

        # Convert PIL to np array
        image_np = np.array(self.image)
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]

        # detection
        detections = self.model(input_tensor)

        # Process detections
        boxes = detections['detection_boxes'][0].numpy()
        classes = detections['detection_classes'][0].numpy().astype(np.int32)
        scores = detections['detection_scores'][0].numpy()

        #  confidence > 50%
        human_detections = [(box, score) for box, cls, score in zip(boxes, classes, scores)
                            if cls == 1 and score > 0.5]  #  1 is 'person' in COCO dataset




        # draw boundings
        image_with_detections = self.draw_boxes(image_np, human_detections)

        # result
        result_image = Image.fromarray(image_with_detections)
        result_photo = ImageTk.PhotoImage(result_image)
        self.detected_image_label.config(image=result_photo)
        self.detected_image_label.image = result_photo

    def draw_boxes(self, image, detections):

        for box, score in detections:
            ymin, xmin, ymax, xmax = box
            im_height, im_width, _ = image.shape
            left, right, top, bottom = int(xmin * im_width), int(xmax * im_width), int(ymin * im_height), int(ymax * im_height)

            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(image, f'{score:.2f}', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        return image

    def return_to_main(self):
        self.destroy()
        self.return_callback()

