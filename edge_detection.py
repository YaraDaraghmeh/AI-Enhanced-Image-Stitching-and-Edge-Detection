import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk


class EnhancedImageProcessingFrame(ttk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master, padding="20")
        self.return_callback = return_callback
        self.selected_image = None
        self.processed_images = {}


        ttk.Label(self, text="Enhanced Image Processing", font=("Arial", 16)).pack(pady=20)


        self.select_button = ttk.Button(self, text="Select Image", command=self.select_image)
        self.select_button.pack(pady=10)


        self.image_frame = ttk.Frame(self)
        self.image_frame.pack(pady=10, fill="x", expand=True)




        self.process_button = ttk.Button(self, text="Process Image", command=self.process_image)
        self.process_button.pack(pady=10)

        # kernel size initially
        self.kernel_size_var = tk.IntVar(value=3)
        self.kernel_size_slider = ttk.Scale(self, from_=3, to=15, orient="horizontal",
                                            variable=self.kernel_size_var, command=self.update_kernel_size)
        self.kernel_size_slider.pack(pady=10)
        ttk.Label(self, text="Kernel Size").pack()


        ttk.Button(self, text="Back to Main", command=self.return_to_main).pack(pady=5)

    def select_image(self):
        #  file dialog to select an image
        filetypes = [("Image files", "*.jpg *.jpeg *.png")]
        filename = filedialog.askopenfilename(title="Select an image for processing", filetypes=filetypes)

        if filename:
            self.selected_image = cv2.imread(filename)
            self.display_selected_image(filename)
        else:
            messagebox.showinfo("Info", "No image selected")

    def display_selected_image(self, img_path):
        # clear previous selected imag
        for widget in self.image_frame.winfo_children():
            widget.destroy()


        img = Image.open(img_path)
        img.thumbnail((200, 200))  # Resize the image thumbnail
        photo = ImageTk.PhotoImage(img)

        label = ttk.Label(self.image_frame, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack(side=tk.LEFT, padx=2)

        ttk.Label(self.image_frame, text="Selected Image").pack(side=tk.LEFT, padx=5)

    def process_image(self):
        if self.selected_image is None:
            messagebox.showerror("Error", "Please select an image first")
            return

        # Canny
        canny_edges = cv2.Canny(self.selected_image, 100, 200)

        #  (DoG)
        gray = cv2.cvtColor(self.selected_image, cv2.COLOR_BGR2GRAY)
        gaussian1 = cv2.GaussianBlur(gray, (5, 5), 0)
        gaussian2 = cv2.GaussianBlur(gray, (9, 9), 0)
        dog = gaussian1 - gaussian2

        # Apply morphological operation (initially with 3x3 kernel)
        kernel = np.ones((3, 3), np.uint8)
        dog_morphed = cv2.morphologyEx(dog, cv2.MORPH_CLOSE, kernel)


        self.processed_images = {
            'canny': canny_edges,
            'dog': dog,
            'dog_morphed': dog_morphed
        }


        self.display_results()

    def display_results(self):
        # Create a new window for displaying results
        results_window = tk.Toplevel(self)
        results_window.title("Processing Results")


        # Canny Edge Detection result
        self.display_image(results_window, self.processed_images['canny'], "Canny Edge Detection")

        #   DoG result
        self.display_image(results_window, self.processed_images['dog'], "Difference of Gaussians (DoG)")

        # Morphed DoG result
        self.morphed_label = self.display_image(results_window, self.processed_images['dog_morphed'], "Morphed DoG")

        #  slider to adjust kernel size
        ttk.Label(results_window, text="Adjust Kernel Size:").pack(pady=5)
        kernel_slider = ttk.Scale(results_window, from_=3, to=15, orient="horizontal",
                                  command=lambda x: self.update_morphology(int(float(x))))
        kernel_slider.set(3)  # Initial value
        kernel_slider.pack(pady=5)

    def display_image(self, window, image, title):
        cv2.imwrite('temp.png', image)
        img = Image.open('temp.png')
        img.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(img)
        label = ttk.Label(window, image=photo)
        label.image = photo
        label.pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Label(window, text=title).pack(side=tk.LEFT, padx=10)
        return label

    def update_morphology(self, kernel_size):
        if kernel_size % 2 == 0:
            kernel_size += 1  # Ensure odd kernel size
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        dog_morphed = cv2.morphologyEx(self.processed_images['dog'], cv2.MORPH_CLOSE, kernel)

        # update displayed image
        cv2.imwrite('temp.png', dog_morphed)
        img = Image.open('temp.png')
        img.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(img)
        self.morphed_label.configure(image=photo)
        self.morphed_label.image = photo

    def update_kernel_size(self, value):
        #  method is called when the slider value changes
        kernel_size = int(float(value))
        if kernel_size % 2 == 0:
            kernel_size += 1  # Ensure odd kernel size
        self.kernel_size_var.set(kernel_size)

    def return_to_main(self):

        self.destroy()
        self.return_callback()